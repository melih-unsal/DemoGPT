from .task_definitions import TASK_DESCRIPTIONS

system_template = f"""
Refine the Generated Task List according to the Feedback

Task objects must be Python dictionaries, and the output should strictly conform to a Python list of JSON objects.
So use double quotes because this output will be converted to json with json.loads function.

It is extremely important to include these keys in each task object:

-step
-task_type
-task_name
-input_key
-input_data_type
-output_key
-output_data_type
-description

################################

Available Tasks:

{TASK_DESCRIPTIONS}
"""

human_template = """
Instruction:{instruction}
################################
Generated Task List:
{tasks}
################################
Feedback given to the Generated Task (extremly important) : {feedback}
################################
New Refined Task List:
"""
