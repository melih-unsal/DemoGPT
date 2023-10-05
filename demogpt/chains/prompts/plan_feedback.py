system_template = """
Generate a feedback JSON to the given plan which is prepared for the given instruction.
The JSON includes 2 keys which are "success" and "feedback".
"feedback" corresponds to the feedback to the plan.
"success" corresponds to the success of the plan. If the plan is good then "success" should be True. Otherwise, it should be False. 

In each step, there are tasks in the below format:
[$task_name($args) ---> $output]

You should check 2 things.

1.Only those task names are allowed to be used:
{TASK_NAMES}

2. If one of the task's output is  input of another, then output_data_type of previous one
should be the same as input_data_type of successor.
These are the data types:
{TASK_DTYPES}
"""

human_template = """
Instruction: {instruction}
Plan:{plan}
Feedback JSON:
"""
