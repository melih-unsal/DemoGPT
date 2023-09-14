human_template = """
variable: url
instruction: Get website URL from the user
code:
url = st.chat_input("Enter website URL")

variable: source_text
instruction: Get source text from the user
code:
source_text = st.chat_input("Type the source text")

variable: input_language
instruction: Get the input language from the user
code:
input_language = st.chat_input("Enter the input language")

variable: {variable}
instruction: {instruction}
code:

"""