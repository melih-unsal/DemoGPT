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
# Assume that, they have been already defined but only call the function by checking if the input is not an empty string.
# use st.markdown to show the main text
#
# Here is the part of the code that you are supposed to continue:
# {code_snippets}
#
# Instruction:{instruction}
# Streamlit Code:
# """

human_template = """
args: next_segment
instruction: Display the generated next narrative segment to the user
code:
if next_segment:
    st.success(next_segment)
        
args: medium_article
instruction: Display the generated Medium article to the user
code:
if submitted:
    st.markdown(medium_article)
        
args: translated_text
instruction: Display the translated text to the user
code:
if translated_text:
    st.info(translated_text)

args:{args}
instruction:{instruction}
code:

"""
