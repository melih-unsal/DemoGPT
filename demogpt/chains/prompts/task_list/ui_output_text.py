# human_template = """
# Write and call a function which shows text by streamlit text element code depending on the instruction below:
# Suppose that, streamlit has been imported by "import streamlit as st" so you don't need to import it.
#
# The function arguments are "{args}".
# You can assume that the variables with the same names are already defined.
# So you don't need to give dummy variables to the function while calling.
# You should use "{args}" to call the function
# In the function, also add a descriptive part next to the "{args}"
# After defining the function, call it with "{args}".
# Assume that, they have been already defined but only call the function by checking if the is not None and len(str(the)) > 0 input is not an empty string.
# use st.markdown to show the main text
#
# Here is the part of the code that you are supposed to continue:
# {code_snippets}
#
# Instruction:{instruction}
# Streamlit Code:
# """

system_template = """
You cannot use other st.func_name even if it is image or table or any kind. You are supposed to select one of most appropriate one in the followings:
[st.markdown, st.header, st.subheader, st.caption, st.code, st.text, st.latext, st.write]
"""

human_template = """
args: next_segment
data type: string
instruction: Display the generated next narrative segment to the user
code:
if next_segment is not None and len(str(next_segment)) > 0:
    st.success(next_segment)

args:{args}
data type: {data_type}
instruction:{instruction}
code:

"""
