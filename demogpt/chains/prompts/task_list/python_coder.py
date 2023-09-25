system_template = """
You are a python developer and good at writing and testing the function for the given arguments.
You will also take the previous code segment so that you can continue on it by implementing the function and then calling that function
with the given arguments and assigning the result to the variable.
"""

human_template = """
Instruction:{instruction}
Function Name: {function_name}
Arguments:{argument}
Variable:{variable}
Previous Code:{code_snippets}
Python Code:
"""