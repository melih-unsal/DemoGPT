from .task_definitions import TASK_DESCRIPTIONS, TASK_DTYPES, TASK_NAMES

system_template = f"""
Create a plan to fulfill the given instruction by considering the first plan and the feedback given to the plan. 
The plan should be broken down into clear, logical steps that detail how to accomplish the task. 
Consider all necessary user interactions, system processes, and validations, 
and ensure that the steps are in a logical sequence that corresponds to the given instruction.
Don't generate impossible steps in the plan because only those tasks are available:
{TASK_DESCRIPTIONS}

Pay attention to the input_data_type and the output_data_type.
If one of the task's output is  input of another, then output_data_type of previous one
should be the same as input_data_type of successor.

Only those task types are allowed to be used:
{TASK_NAMES}

Highly pay attention to the input data type and the output data type of the tasks while creating the plan. These are the data types:

{TASK_DTYPES}

When you create a step in the plan, its input data type 
either should be none or the output data type of the caller step. 

If you use a task in a step, highly pay attention to the input data type and the output data type of the task because it should be compatible with the step.
The refined plan should have the same structure as the draft plan.
"""

human_template = """
Don't generate redundant steps which is not meant in the instruction.
Keep in mind that for chat-based app where conversation history is really important, you must use those task types below:
"chat", "ui_input_chat" and "ui_output_chat". For chat-based inputs, use "ui_input_chat" and chat-based outputs use "ui_output_chat"

Instruction: {instruction}
Draft Plan: {plan}
Feedback: {feedback}
Let’s think step by step.
Refined Plan:
"""
