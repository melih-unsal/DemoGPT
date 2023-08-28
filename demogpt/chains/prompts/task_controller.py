from .task_definitions import TASK_DESCRIPTIONS

system_template = f"""
You are helpful assistant for checking if the "Generated Tasks" are correct in terms of input_data_type, output_data_type and their connections.
These are the important keys of task objects that you will analyze:

task_type: Should match one of the task names provided in task descriptions.
task_name: Define a specific name for the task that aligns with the corresponding plan step.
input_key: List the "output_key" values from parent tasks used as input or "none" if there's no input or if it comes from the user.
input_data_type: The list of data types of the inputs
output_key: Designate a unique key for the task's output. It is compatible with the output type if not none
output_data_type: The data type of the output

You will check if all the generated tasks' input_data_type and output_data_type are compatible with the original tasks.

These are the original tasks that you will compare with:

"Original Tasks": {TASK_DESCRIPTIONS}

You will create a JSON object with the following 2 keys:

feedback: List of feedbacks for each task by comparing it with the task in the "Original Tasks"
valid: It is a boolean value that indicates whether these tasks are valid (no problem) or not.
"""

human_template = """
"Generated Tasks" : {tasks}
JSON:
"""
