from chains.task_definitions import TASK_DESCRIPTIONS

system_template = f"""
Create a python list of task objects where task objects are python dictionaries
You can only use those tasks below:

{TASK_DESCRIPTIONS}

Make sure the output is stritly in Python list of JSON objects
"""

human_template = """
Create a list for of task objects to accomplish the instruction according to the plan.
Don't create any redundant task, only create the needed the high level tasks.
For each step in the plan, generate a corresponding task object

Task objects are python dictionaries having "task_type", "task_name", "input_key", "output_key", "description"

"task_type" is the type of the task. This is one of the "name" in the available tasks.
"task_name" is the name of the task
"input_key" is the list of output_key from parent tasks used as an input. 
Every element should be an output_key of another task unless the input is coming from the user. When it is coming from the user, make it "none". 
If there is no input, make it "none"
"output_key" is the unique output of the model.
"description" goal of the task (sub instruction)

Create at least 1 task per plan step to be sure that the plan is fully applied.

##########################
Instruction:{instruction}
##########################
Plan : {plan}
##########################
List of Task objects(List of JSON):
"""