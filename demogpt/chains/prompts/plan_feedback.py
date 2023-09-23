from .task_definitions import TASK_DESCRIPTIONS, TASK_DTYPES, TASK_NAMES

system_template = f"""
Generate a feedback to the given plan which is prepared for the given instruction.
The plan should be broken down into clear, logical steps that detail how to accomplish the task. 
Consider all necessary user interactions, system processes, and validations, 
and ensure that the steps are in a logical sequence that corresponds to the given instruction.
While generating the feedback consider that only those tasks are available:
{TASK_DESCRIPTIONS}

Pay attention to the input_data_type and the output_data_type.
If one of the task's output is input of another, then output_data_type of previous one
should be the same as input_data_type of successor.

Only those task types are allowed to be used:
{TASK_NAMES}

Highly pay attention to the input data type and the output data type of the tasks while creating the plan. These are the data types:

{TASK_DTYPES}

If you think that, the plan is meeting all the necessary steps and inclusive then only say "<SUCCESS>".
Otherwise, give a feedback.
"""

human_template = """
Instruction: {instruction}
Plan:{plan}
Feedback:
"""