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
                
    all_input_keys = set(all_input_keys) 
    all_input_keys.add("none")
    
    feedback = ""
    
    for task in tasks:
        if task["output_key"] not in all_input_keys:
            feedback += f"Task {task['task_name']} is redundant because its output is never used. Try another approach.\n"
            
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
    task_prompt_template = any([task["task_type"] == "prompt_template" for task in tasks])
    task_chat = any([task["task_type"] == "chat" for task in tasks])
    task_search = any([task["task_type"] == "google_search" for task in tasks])
    
    app_prompt_template = 0 # neutral
    
    app_chat = app_type["is_chat"]["value"] == "true"
    app_search = app_type["is_search"]["value"] == "true"
    if not app_chat:
        if app_type["is_ai"]["value"] == "true":
            app_prompt_template = 1
        else:
            app_prompt_template = -1
    
    feedback = ""
    if app_chat:
        if not task_chat:
            feedback += "The app is chat-based but you didn't use 'chat' in your tasks. Please add it and try again"
    else:
        if task_chat:
            feedback += "The app is not chat-based but you used chat related tasks in your task list. Please remove them and try again"
    ################################################################################################################################################
    if app_search:
        if not task_search:
            feedback += "The app is search-based but you didn't use 'google_search' in your tasks. Please add it and try again"
    else:
        if task_search:
            feedback += "The app is not search-based but you used 'google_search' task in your task list. Please remove them and try again"
    ################################################################################################################################################
    if app_prompt_template == 1:
        if not task_prompt_template:
            feedback += "The app is ai-based but you didn't use 'prompt_template' in your tasks. Please add it and try again"
    elif app_prompt_template == -1:
        if task_prompt_template:
            feedback += "The app is not ai-based but you used 'prompt_template' in your tasks which is redundant. Please remove it and try again"
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
