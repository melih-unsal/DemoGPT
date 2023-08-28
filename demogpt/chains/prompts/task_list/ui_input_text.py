human_template = """
Write a streamlit textfield or textarea code depending on the instruction below:
Suppose that, streamlit has been imported by "import streamlit as st" so you don't need to import it.
Here is the part of the code that you are supposed to continue:
{code_snippets}

Assign the taken input to the variable called "{variable}"

Instruction:{instruction}
Streamlit Code:
"""
