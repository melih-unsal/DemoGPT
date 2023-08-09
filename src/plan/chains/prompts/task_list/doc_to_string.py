system_template = """
You are a good Python developer and your task is creating and calling a function called {function_name},
which converts Document object to a string.
You can easily doncert Document object to string by well-known str() function.
Use that function according to the given argument and variable name.
You will assign {variable} to the string version of {argument}.

Here is the part of the code that you are supposed to continue:
{code_snippets}
"""

human_template = """
Argument:{argument}
Variable:{variable}
Python Code:
"""