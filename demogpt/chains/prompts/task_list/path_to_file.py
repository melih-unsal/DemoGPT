system_template = """
You are good at writing Python code.
You are supposed to create a function and call that function which does
the given instruction.
Here is the part of the code that you are supposed to continue:
{code_snippets}
"""

human_template = """
Write a function to load the file from the path for the argument name, variable and instruction below and also check if the path is not empty:
Instruction:{instruction}
Argument Name : {argument}
Variable Name : {variable}
Python Code:
"""
