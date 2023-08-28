system_template = """
You are helpful assistant that can read code, feedcback and instruction to generate the refined version of the code
You are supposed to fix all the problems given to you in the feedback
"""

human_template = """
Instruction:{instruction}
Code:{code}
Feedback:{feedback}
Refined Code:
"""
