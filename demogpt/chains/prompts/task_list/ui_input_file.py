system_template = """
Write a streamlit file uploader code and return the path of uploaded file as a string depending on the instruction given to you:
Since st.file_uploader.name does not give full file path, you first need to save it then get a full file path like in the following:

uploaded_file = st.file_uploader("Upload Txt File", type=["txt"])
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        {variable} = temp_file.name # it shows the file path
else:
    {variable} = ''

Suppose that, streamlit has been imported by "import streamlit as st" so you don't need to import it.
Here is the part of the code that you are supposed to continue:
{code_snippets}

Assign the file path to the variable called "{variable}"
You will basically use file_uploader and get file path from it but nothing else.
Not to loose the file path, please use st.session_state[<key>]
Don't read the file, only get the file path
"""

human_template = """
Instruction:{instruction}
Streamlit Code:
"""
