system_template = """
Create a plan to fulfill the given instruction by considering the Problematic Plan and the Problems it has. 
The plan should be broken down into clear, logical steps that detail how to accomplish the task. 
Consider all necessary user interactions, system processes, and validations, 
and ensure that the steps are in a logical sequence that corresponds to the given instruction.

Each step can only use on of the functions below:

{TASK_NAMES}

These are the explanations of those functions:

{TASK_PURPOSES}

Your main job is by considering the "Problems", generating new plan
Please ensure that the New Refined Plan does not contain any problem mentioned in the "Problems".
If needed, you can change the number of steps, remove/replace/add steps as long as you use only the allowed functions
"""

human_template = """
Instruction:{instruction}

Problematic Plan:
{plan}

Problems: {feedback}

New Refined Plan:
"""
