human_template = """
variable: url
instruction: Get website URL from the user
code:
if url := st.chat_input("Enter website URL"):
    with st.chat_message("user"):
        st.markdown(url)
    st.session_state.messages.append({{"role": "user", "content": url}})

variable: source_text
instruction: Get source text from the user
code:
if source_text := st.chat_input("Type the source text"):
    with st.chat_message("user"):
        st.markdown(source_text)
    st.session_state.messages.append({{"role": "user", "content": source_text}})

variable: input_language
instruction: Get the input language from the user
code:
if input_language := st.chat_input("Enter the input language"):
    with st.chat_message("user"):
        st.markdown(input_language)
    st.session_state.messages.append({{"role": "user", "content": input_language}})

variable: {variable}
instruction: {instruction}
code:

"""