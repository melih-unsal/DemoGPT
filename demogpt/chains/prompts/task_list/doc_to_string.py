system_template = """
You are a good Python developer and your task is creating and calling a function called {function_name},
which converts Document object to a string.
You can easily convert Document object docs to string like in the following:

{variable} = "\".join([doc.page_content for doc in {argument}])

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
