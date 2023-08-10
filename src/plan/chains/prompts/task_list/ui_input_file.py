human_template = """
Write a streamlit file uploader code and return the path of uploaded file as a string depending on the instruction given to you:
Since st.file_uploader.name does not give full file path, you first need to save it then get a full file path.
Suppose that, streamlit has been imported by "import streamlit as st" so you don't need to import it.
Here is the part of the code that you are supposed to continue:
{code_snippets}

Assign the file path to the variable called "{variable}"
You will basically use file_uploader and get file path from it but nothing else.
Not to loose the file path, please use st.session_state[<key>]
Don't read the file, only get the file path

Instruction:{instruction}
Streamlit Code:
"""
