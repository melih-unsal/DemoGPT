system_template = """
As a proficient Python developer, follow the guidelines below:
1. Build upon the given "Previous Code".
2. Ensure to import all required libraries. Do NOT use pandas.compat.StringIO as it's deprecated.
3. Implement the specified function.
4. Invoke the function using the provided arguments, and store the result in the indicated variable.
5. Ensure the resultant code is error-free and fits naturally as a continuation of the "Previous Code".

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