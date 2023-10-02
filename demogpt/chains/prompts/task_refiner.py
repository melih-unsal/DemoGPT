system_template = """
Refine the Generated Task List by fixing the problem mentinoed in the Feedback

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

You are only allowed to use those tasks below:

{TASK_NAMES}

These are the explanations of those tasks:

{TASK_PURPOSES}

Your main job is by considering the "Problems", generating new task list
Please ensure that the New Refined Task List does not contain any problem mentioned in the "Problems".
If needed, you can change the number of tasks, remove/replace/add tasks as long as you use only the allowed tasks
"""

human_template = """
Instruction:{instruction}
################################
Problematic Task List:
{tasks}
################################
Problems: {feedback}
################################
New Refined Task List:
"""
