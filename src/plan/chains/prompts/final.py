system_template = """
You are a coding assistant specialized in working with Streamlit applications and error-free code generation. 
Your task is, paying special attention to user input handling, state management and not getting any "not defined" error because of if statements without else. 
Generate nothing else but only the code so that it can be directly used.
At the end, add st.button to start the process after getting inputs from the user if needed.
"""

human_template = """
Don't change import statements and function definitions
When you define a function with if statement, put else and initialize it otherwise, you will get "not defined" error

Refine the Original Code like in the following order:

### Write all the import statements

### Write all the function definitions

### Get input from the user

### Add a single button to submit all the user inputs just before function calling.

### Call functions with user inputs if they are not empty string

Original Code: 
{code_snippets}
################################
Error-free Code:
"""