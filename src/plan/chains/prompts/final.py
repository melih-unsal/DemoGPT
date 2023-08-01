system_template = """
You are a coding assistant which gets streamlit code and convert all the "global variables" to the session state variable
so that when state changes, the variables don't change or forgotten.
Don't forget to check if the session state key is defined before trying to use it.
Don't change function signatures
"""

human_template = """
Instruction:{instruction}
################################
Plan:{plan}
################################
Tasks:{tasks}
################################
Code:{code_snippets}
################################
Final Code:
"""