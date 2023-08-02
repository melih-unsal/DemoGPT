human_template = """
Write a streamlit file uploader code and read the content of the uploaded file and returns its content as a string depending on the instruction below:
Suppose that, streamlit has been imported by "import streamlit as st" so you don't need to import it.

Assign the taken input to the variable called "{variable}"
Return file content as string

Instruction:{instruction}
Streamlit Code:
"""