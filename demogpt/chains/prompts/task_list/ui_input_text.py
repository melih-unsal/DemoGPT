# human_template = """
# Write a streamlit textfield or textarea code depending on the instruction below:
# Suppose that, streamlit has been imported by "import streamlit as st" so you don't need to import it.
# Here is the part of the code that you are supposed to continue:
# {code_snippets}
#
# Assign the taken input to the variable called "{variable}"
#
# Instruction:{instruction}
# Streamlit Code:
# """

human_template = """
variable: url
instruction: Get website URL from the user
code:
url = st.text_input("Enter website URL")

variable: source_text
instruction: Get source text from the user
code:
source_text = st.text_area("Enter source text")

variable: input_language
instruction: Get the input language from the user
code:
input_language = st.text_input("Enter the input language")

variable: color
instruction: Select the color
code:
color = st.selectbox("Select the color", ["Red", "Blue", "Green", "Yellow", "purple"])

variable: {variable}
instruction: {instruction}
code:

"""
