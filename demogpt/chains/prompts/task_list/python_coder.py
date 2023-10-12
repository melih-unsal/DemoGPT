system_template = """
As a proficient Python developer, follow the guidelines below:
1. Build upon the given "Previous Code".
2. Ensure to import all required libraries. Do NOT use pandas.compat.StringIO as it's deprecated.
3. Implement the specified function.
4. Check if the arguments are valid (not None and/or non empty)
5. If the arguments are valid, invoke the function using the provided arguments, and store the result in the indicated variable. Otherwise, assign an empty string to the indicatd variable 
5. Ensure the resultant code is error-free and fits naturally as a continuation of the "Previous Code".


It should be the complete version of this:
================================================================
# all library imports
def {function_name}({argument}):
    # complete the function and return the result
    
if {argument} is not None and len({argument}) > 0:
    {variable} = {function_name}({argument})
else:
    {variable} = ''
================================================================
Import all the Python libraries you use in the result.
Your generated function cannot be empty and should be functional. So, you cannot generate a function having only comments.
    
Let's get coding!
"""

human_template = """
Instruction: {instruction}
Function Name: {function_name}
Arguments: {argument}
Assigned Variable: {variable}
Previous Code:
{code_snippets}
Python Code Continuation:
"""
