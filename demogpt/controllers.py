import re

from demogpt.chains.prompts.task_definitions import TASK_TYPE2_TASK

def checkRedundantTasks(tasks):
    all_input_keys = []
    for task in tasks:
        inputs = task["input_key"]
        if inputs == "none":
            inputs = []
        else:
            if isinstance(inputs, str):
                if inputs.startswith("["):
                    inputs = inputs[1:-1]
                all_input_keys += [var.strip() for var in inputs.split(",")]
            else:
                all_input_keys += inputs
                
    all_input_keys = set(all_input_keys) 
    all_input_keys.add("none")
    
    feedback = ""
    
    for task in tasks:
        if isinstance(task["output_key"],str):
            if task["output_key"] not in all_input_keys:
                feedback += f"Task {task['task_name']} is redundant because its output is never used. Try another approach.\n"
        elif isinstance(task["output_key"],list):
            for output_key in task["output_key"]:
                if output_key not in all_input_keys:
                    feedback += f"Task {task['task_name']} has problem because its output {output_key} is never used. Try another approach.\n"
            
    valid = len(feedback) == 0
    
    return {"feedback": feedback, "valid": valid}

def refineKeyTypeCompatiblity(task):
    if task["input_data_type"] == "none":
        if task["input_key"] != "none":
            task["input_key"] = "none"
    if task["output_data_type"] == "none":
        if task["output_key"] != "none":
            task["output_key"] = "none"
    return task   

def checkAppTypeCompatiblity(tasks, app_type):
    must_chat_tasks = {"ui_input_chat","chat", "ui_output_chat"}
    must_prompt_template_tasks = {"prompt_template"}
    must_search_tasks = {"google_search"}
    
    task_types = set([task["task_type"] for task in tasks])
    
    task_prompt_template = must_prompt_template_tasks & task_types
    task_search =  must_search_tasks & task_types
    task_chat = must_chat_tasks & task_types
    
    
    app_prompt_template = 0 # neutral
    
    app_chat = app_type["is_chat"]["value"] == "true"
    app_search = app_type["is_search"]["value"] == "true"
    if not app_chat:
        if app_type["is_nlp"]["value"] == "true":
            app_prompt_template = 1
        else:
            app_prompt_template = -1
    
    feedback = ""

    if app_chat:
        for task_type in must_chat_tasks - task_chat:
            feedback += f"The app is chat-based but you didn't use {task_type} in your tasks. Please add it and try again"
    else:
        for task_type in task_chat:
            feedback += f"The app is not chat-based but you used {task_type} in your task list. Please remove it and try again"
    ################################################################################################################################################
    if app_search:
        for task_type in must_search_tasks - task_search:
            feedback += f"The app is search-based but you didn't use {task_type} in your tasks. Please add it and try again"
    else:
        for task_type in task_search:
            feedback += f"The app is not search-based but you used {task_type} task in your task list. Please remove them and try again"
    ################################################################################################################################################
    if app_prompt_template == 1:
        for task_type in must_prompt_template_tasks - task_prompt_template:
            feedback += f"The app is ai-based but you didn't use {task_type} in your tasks. Please add it and try again"
    elif app_prompt_template == -1:
        for task_type in task_prompt_template:
            feedback += f"The app is not ai-based but you used {task_type} in your tasks which is redundant. Please remove it and try again"
    ################################################################################################################################################
    
    valid = len(feedback) == 0
    
    return {"feedback": feedback, "valid": valid}
                

def checkDTypes(tasks):

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
            if isinstance(input_key, str):
                if input_data_type != reference_input and input_data_type != "none":
                    feedback += f"""
                    {name} expects all inputs as {reference_input} or none but the data type of {input_key} is {input_data_type} not {reference_input}. Please find another way.\n
                    """
            else:
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
    template_inputs =  inputs + additional_inputs
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
