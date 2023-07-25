human_template = """
Replace the functions in the Streamlit Code with the same functions names in the LangChain Code
All the library imports are given to you
Remove unused functions

Instruction:{instruction}
Streamlit Code:{streamlit_code}
LangChain Code:{langchain_code}
All imports:{imports_code_snippet}

Final Streamlit Code:
"""