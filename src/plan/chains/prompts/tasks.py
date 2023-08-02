from chains.task_definitions import TASK_DESCRIPTIONS

system_template = f"""
Create a Python list of task objects that align with the provided instruction and plan. Task objects must be Python dictionaries, and the output should strictly conform to a Python list of JSON objects.

You must use only the tasks provided in the description:

{TASK_DESCRIPTIONS}
"""

human_template = """
Create a Python list of task objects that align with the provided instruction and all steps of the plan.

Task objects must be Python dictionaries, and the output should strictly conform to a Python list of JSON objects.

Follow these detailed guidelines:

Task Objects: Create a Python dictionary for each task using the following keys:

step: It represents the step number corresponding to which plan step it matches
task_type: Should match one of the task names provided in task descriptions.
task_name: Define a specific name for the task that aligns with the corresponding plan step.
input_key: List the "output_key" values from parent tasks used as input or "none" if there's no input or if it comes from the user.
output_key: Designate a unique key for the task's output.
description: Provide a brief description of the task's goal, mirroring the plan step.

Ensure that each task corresponds to each step in the plan, and that no step in the plan is omitted.

##########################
Instruction:{instruction}
##########################
Plan : {plan}
##########################
List of Task Objects (Python List of JSON), and ensure that each task corresponds to each step in the plan:
"""