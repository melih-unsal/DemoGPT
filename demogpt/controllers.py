import re
from functools import reduce
from demogpt.chains.task_definitions import getTasks

def planToTaskFormat(plan):
    pattern = re.compile(r"\b(\w+)\(([^)]*)\)( ---> ([\w_,\s]+))?")
    matches = pattern.findall(plan)
    functions = [
        {
            "name": match[0],
            "arguments": [
                arg.strip()
                for arg in match[1].split(",")
                if arg.strip() and '"' not in arg.strip()
            ],
            "output": [
                arg.strip()
                for arg in match[3].split(",")
                if arg.strip() and '"' not in arg.strip()
            ],
        }
        for match in matches
    ]
    plan_steps = []
    for i, function in enumerate(functions):
        step = {
            "step": i + 1,
            "task_type": function["name"],
            "task_name": function["name"],
            "input_key": function["arguments"],
            "output_key": function["output"],
        }
        plan_steps.append(step)
    return plan_steps

def checkTaskNames(tasks, app_type):
    TASK_TYPE2_TASK = getTasks(app_type)[-1]
    feedback = ""
    for task in tasks:
        name = task["task_type"]
        if name not in TASK_TYPE2_TASK:
            feedback += f"Task {name} is invalid, you cannot use undefined task.\n"
            
    if feedback:
        feedback += "\nOnly those tasks are available:" + " ".join(
                TASK_TYPE2_TASK.keys()
            )
    
    valid = len(feedback) == 0
    
    return {
        "feedback": feedback,
        "valid": valid
    }

def validate(input, app_type):
    if isinstance(input,str):#means plan
        input = planToTaskFormat(input) 
    
    res1 = checkTaskNames(input, app_type)
    res2 = checkAppTypeCompatiblity(input, app_type)
    res3 = checkRedundantTasks(input)
    res4 = checkInputOutputLengthCompatiblity(input, app_type)
    res5 = checkInputOuputCompatibility(input)

    feedback = ""
    
    if not res1["valid"]:
        feedback += "\n" + res1["feedback"]
    if not res2["valid"]:
        feedback += "\n" + res2["feedback"]
    if not res3["valid"]:
        feedback += "\n" + res3["feedback"]
    if not res4["valid"]:
        feedback += "\n" + res4["feedback"]
    if not res5["valid"]:
        feedback += "\n" + res5["feedback"]

    valid = len(feedback) == 0
    
    print("feedback:")
    print(feedback)

    return {"feedback": feedback, "valid": valid}

def refineKeyTypeCompatiblity(task):
    if task["input_data_type"] == "none":
        if task["input_key"] != "none":
            task["input_key"] = "none"
    if task["output_data_type"] == "none":
        if task["output_key"] != "none":
            task["output_key"] = "none"
    return task


def checkInputOuputCompatibility(tasks):
    feedback = ""
    inputs = set((reduce((lambda x, y: x+y),[task["input_key"] for task in tasks] + [["none"]])))
    outputs = set((reduce((lambda x, y: x+y),[task["output_key"] for task in tasks] + [["none"]])))
        
    input2tasks = {}
    output2tasks = {}
    for task in tasks:
        for input_key in task["input_key"]:
            input_task_names = input2tasks.get(input_key,[])
            input_task_names.append(task["task_name"])
            input2tasks[input_key] = input_task_names
        for output_key in task["output_key"]:
            output_task_names = output2tasks.get(output_key,[])
            output_task_names.append(task["task_name"])
            output2tasks[output_key] = output_task_names
    
    ghost_inputs = inputs - outputs # inputs which are not coming from output of another task
    redundant_outputs = outputs - inputs # outputs which are an input of another task
    
    for input_key in ghost_inputs:
        for task_name in input2tasks[input_key]:
            feedback += f"Remove task {task_name} because its input {input_key} is not coming from another task.\n" 
    for output_key in redundant_outputs:
        for task_name in output2tasks[output_key]:
            feedback += f"Remove task {task_name} because its output {output_key} is not used. It is redundant.\n" 
    
    valid = len(feedback) == 0
    
    return {
        "valid": valid,
        "feedback": feedback
    }
        

def checkRedundantTasks(tasks):
    all_input_keys = []
    for task in tasks:
        inputs = task["input_key"]
        all_input_keys += inputs

    all_input_keys = set(all_input_keys)
    all_input_keys.add("none")

    feedback = ""

    for task in tasks:
        for output_key in task["output_key"]:
            if output_key not in all_input_keys:
                feedback += f"Task {task['task_name']} has problem because its output {output_key} is never used. Try another approach.\n"

    valid = len(feedback) == 0

    return {"feedback": feedback, "valid": valid}

def checkInputOutputLengthCompatiblity(tasks, app_type):
    TASK_TYPE2_TASK = getTasks(app_type)[-1]
    feedback = ""
    for task in tasks:
        task_type = task["task_type"]
        if task_type not in TASK_TYPE2_TASK:
            continue
        
        original_task = TASK_TYPE2_TASK[task_type]
        # input check
        if original_task["input_data_type"] == "none":
            if len(task["input_key"]) > 0:
                feedback += f"Task {task_type} cannot have input\n"
        
        elif not original_task["input_data_type"].startswith("*"):
            if len(task["input_key"]) > 1:
                feedback += f"Task {task_type} can only have single input but you gave multiple"
                
        # output check
        if original_task["output_data_type"] == "none":
            if len(task["output_key"]) > 0:
                feedback += f"Task {task_type} cannot have output\n"
                
        elif not original_task["output_data_type"].startswith("*"):
            if len(task["output_key"]) > 1:
                feedback += f"Task {task_type} can only have single output but you gave multiple"
                
    valid = len(feedback) == 0
    
    return {
        "feedback": feedback,
        "valid": valid
    }
    

def checkAppTypeCompatiblity_old(tasks, app_type):
    must_chat_tasks = {"ui_input_chat", "chat", "ui_output_chat"}
    must_prompt_template_tasks = {"prompt_template"}
    must_search_tasks = {"plan_and_execute"}

    task_types_list= [task["task_type"] for task in tasks]
    task_types = set(task_types_list)

    task_prompt_template = must_prompt_template_tasks & task_types
    task_search = must_search_tasks & task_types
    task_chat = must_chat_tasks & task_types

    app_prompt_template = 0  # neutral

    app_chat = app_type["is_chat"] == "true"
    app_search = app_type["is_search"] == "true"
    if not app_chat:
        if app_type["is_ai"] == "true":
            app_prompt_template = 1
        else:
            app_prompt_template = -1

    feedback = ""
    ################################################################################################################################################
    # chat app check
    if app_chat:
        for task_type in must_chat_tasks - task_chat:
            feedback += f"The app is chat-based but you didn't use {task_type} in your tasks. Please add it and try again\n"
            
        for task_type in must_chat_tasks:
            if task_types_list.count(task_type) > 1:
                feedback += f"You can use {task_type} in your tasks only once. Please remove the redundant ones and combine in a single task\n"
    else:
        for task_type in task_chat:
            feedback += f"The app is not chat-based but you used {task_type} in your task list. Please remove it and try again\n"
    ################################################################################################################################################
    # search app check
    if app_search:
        for task_type in must_search_tasks - task_search:
            feedback += f"The app requires {task_type} task but you didn't use {task_type} in your tasks. Please add it and try again\n"
    else:
        for task_type in task_search:
            feedback += f"The app does not need {task_type} task but you used {task_type} task in your task list. Please remove them and try again\n"
    ################################################################################################################################################
    # prompt_template app check
    if app_prompt_template == 1:
        for task_type in must_prompt_template_tasks - task_prompt_template:
            feedback += f"The app is ai-based but you didn't use {task_type} in your tasks. Please add it and try again\n"
    elif app_prompt_template == -1:
        for task_type in task_prompt_template:
            feedback += f"The app is not ai-based but you used {task_type} in your tasks which is redundant. Please remove it and try again\n"
    ################################################################################################################################################
    # search-python compatiblity
    python_tasks = [task for task in tasks if task["task_type"] == "python"]
    search_tasks = [task for task in tasks if task["task_type"] == "plan_and_execute"]
    found = False
    for python_task in python_tasks:
        python_inputs = set(python_task["input_key"])
        for search_task in search_tasks:
            search_outputs = set(search_task["output_key"])
            if python_inputs & search_outputs:
                feedback += f""" python task '{python_task['task_name']}' uses {(python_inputs & search_outputs).pop()} as an input but it comes from plan_and_execute task '{search_task['task_name']}'. python task cannot use plan_and_execute task's output as an input. Please redesign the tasks so that no python task uses plan_and_execute task's output as an input!"""
                found = True
                break
        if found:
            break

    ################################################################################################################################################
    # plan_and_execute compatibility
    search_indices = sorted([task["step"] for task in search_tasks])
    if len(search_tasks) > 1:
        for index in search_indices:
            if index + 1 in search_indices:
                feedback += """It is not recommended to use back to back "plan_and_execute" tasks because one plan_and_execute can handle generic question by itself. 
                You should combine plan_and_execute tasks in a single task."""
                break

    valid = len(feedback) == 0

    return {"feedback": feedback, "valid": valid}


def checkAppTypeCompatiblity(tasks, app_type):
    must_chat_tasks = {"ui_input_chat", "chat", "ui_output_chat", "search_chat"}
    must_prompt_template_tasks = {"prompt_template"}
    must_search_tasks = {"plan_and_execute", "search_chat"}

    task_types_list= [task["task_type"] for task in tasks]
    task_types = set(task_types_list)

    app_prompt_template = 0  # neutral

    app_chat = app_type["is_chat"] == "true"
    app_search = app_type["is_search"] == "true"
    if not app_chat:
        if app_type["is_ai"] == "true":
            app_prompt_template = 1
        else:
            app_prompt_template = -1
            
    if app_chat:
        if app_search:
            must_search_tasks.remove("plan_and_execute")
            must_chat_tasks.remove("chat")
    else:
        must_search_tasks.remove("search_chat")
        must_chat_tasks.remove("search_chat")
        
    task_prompt_template = must_prompt_template_tasks & task_types
    task_search = must_search_tasks & task_types
    task_chat = must_chat_tasks & task_types        

    feedback = ""
    ################################################################################################################################################
    # chat app check
    if app_chat:
        for task_type in must_chat_tasks - task_chat:
            feedback += f"The app is chat-based but you didn't use {task_type} in your tasks. Please add it and try again\n"
            
        for task_type in must_chat_tasks:
            if task_types_list.count(task_type) > 1:
                feedback += f"You can use {task_type} in your tasks only once. Please remove the redundant ones and combine in a single task\n"
    else:
        for task_type in task_chat:
            feedback += f"The app is not chat-based but you used {task_type} in your task list. Please remove it and try again\n"
    ################################################################################################################################################
    # search app check
    if app_search:
        for task_type in must_search_tasks - task_search:
            feedback += f"The app requires {task_type} task but you didn't use {task_type} in your tasks. Please add it and try again\n"
    else:
        for task_type in task_search:
            feedback += f"The app does not need {task_type} task but you used {task_type} task in your task list. Please remove them and try again\n"
    ################################################################################################################################################
    # prompt_template app check
    if app_prompt_template == 1:
        for task_type in must_prompt_template_tasks - task_prompt_template:
            feedback += f"The app is ai-based but you didn't use {task_type} in your tasks. Please add it and try again\n"
    elif app_prompt_template == -1:
        for task_type in task_prompt_template:
            feedback += f"The app is not ai-based but you used {task_type} in your tasks which is redundant. Please remove it and try again\n"
    ################################################################################################################################################
    # search-python compatiblity
    python_tasks = [task for task in tasks if task["task_type"] == "python"]
    search_tasks = [task for task in tasks if task["task_type"] == "plan_and_execute"]
    found = False
    for python_task in python_tasks:
        python_inputs = set(python_task["input_key"])
        for search_task in search_tasks:
            search_outputs = set(search_task["output_key"])
            if python_inputs & search_outputs:
                feedback += f""" python task '{python_task['task_name']}' uses {(python_inputs & search_outputs).pop()} as an input but it comes from plan_and_execute task '{search_task['task_name']}'. python task cannot use plan_and_execute task's output as an input. Please redesign the tasks so that no python task uses plan_and_execute task's output as an input!"""
                found = True
                break
        if found:
            break

    ################################################################################################################################################
    # plan_and_execute compatibility
    search_indices = sorted([task["step"] for task in search_tasks])
    if len(search_tasks) > 1:
        for index in search_indices:
            if index + 1 in search_indices:
                feedback += """It is not recommended to use back to back "plan_and_execute" tasks because one plan_and_execute can handle generic question by itself. 
                You should combine plan_and_execute tasks in a single task."""
                break

    valid = len(feedback) == 0

    return {"feedback": feedback, "valid": valid}


def checkDTypes(tasks, app_type):
    TASK_TYPE2_TASK = getTasks(app_type)[-1]
    
    feedback = ""
    for task in tasks:
        name = task["task_type"]

        input_data_type = task["input_data_type"]
        output_data_type = task["output_data_type"]
        input_key = task["input_key"]

        if name not in TASK_TYPE2_TASK:
            feedback += (
                f"There is no task with a name {name}.Please find another way.\n"
            )
            continue

        reference = TASK_TYPE2_TASK[name]
        reference_input = reference["input_data_type"]
        reference_output = reference["output_data_type"]

        if task["step"] == 1:
            if input_key != "none":
                feedback += f"Since {name} is the first task, its input data type is supposed to be none but it is {input_key}.Please find another way.\n"

        elif reference_input == "*":
            continue

        elif reference_input.startswith("*") and input_data_type == "list":
            continue
        # Check input data types
        elif reference_input.startswith("*"):
            reference_input = reference_input.replace("*", "")
            for res, data_type in zip(input_key, input_data_type):
                if data_type != reference_input:
                    feedback += f"""
                    {name} expects all inputs as {reference_input} but data type of {res} is {data_type} not {reference_input}. Please find another way.\n
                    """
        elif input_data_type != reference_input:
            feedback += f"""
            {name} expects all inputs as {reference_input} but the data type of {input_key} is {input_data_type} not {reference_input}. Please find another way.\n
            """

        if reference_output == "*":
            continue
        # Check output data types
        elif output_data_type != reference_output:
            if not (reference_output.startswith("*") and output_data_type != "list"):
                feedback += f"""
                {name} should output in {reference_output} data type but it is {output_data_type} not {reference_output}. Please find another way.\n
                """

    valid = len(feedback) == 0

    return {"feedback": feedback, "valid": valid}


def checkPromptTemplates(templates, task, additional_inputs=[]):
    templates = " ".join(list(templates.values()))
    inputs = task["input_key"]
    if inputs == "none":
        inputs = []
    else:
        if isinstance(inputs, str):
            if inputs.startswith("["):
                inputs = inputs[1:-1]
            inputs = [var.strip() for var in inputs.split(",")]
    template_inputs = inputs + additional_inputs
    feedback = ""
    for input_key in template_inputs:
        if f"{{{input_key}}}" not in templates:
            feedback += f"'{{{input_key}}}' is not included in any of the templates. You must add '{{{input_key}}}' inside of at least one of the templates.\n"

    # now detect extras

    matches = set(re.findall(r"\{([^}]+)\}", templates))

    for match in matches:
        if match not in template_inputs:
            feedback += f"'{{{match}}}' cannot be included nowhere in the templates. You must remove '{{{match}}}'.\n"

    valid = len(feedback) == 0

    return {"feedback": feedback, "valid": valid}
