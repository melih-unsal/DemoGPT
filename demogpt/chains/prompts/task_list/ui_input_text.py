system_template = """
You will write a single line streamlit input code such as st.text_input, st.selectbox...
You will do it to accomplish the given instruction. You will see examples. You will also see the previous code
segment that you will continue on. You will only write a single streamlit code by looking both the instruction and the previous code
"""

human_template = """
Previous Code Segment:{code_snippets}

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
