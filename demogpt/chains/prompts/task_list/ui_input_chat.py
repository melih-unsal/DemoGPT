system_template = """
You are an AI agent that can generate single like placeholder text depending on the instruction and the variable name.
"""

human_template = """
#############################
variable: url
instruction: Get website URL from the user
placeholder:Enter website URL
#############################
variable: source_text
instruction: Get source text from the user
placeholder:Type the source text
#############################
variable: input_language
instruction: Get the input language from the user
placeholder:Enter the input language
#############################
variable: {variable}
instruction: {instruction}
placeholder:
"""

code = """
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])
        
if {variable} := st.chat_input("{placeholder}"):
    with st.chat_message("user"):
        st.markdown({variable})
    st.session_state.messages.append({{"role": "user", "content": {variable}}})
"""
