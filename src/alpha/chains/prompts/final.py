human_template = """
Combine the Streamlit Code and the LangChain Code 
by taking the pipeline explanation into an account to do the instruction 
All the library imports are given to you
Remove unused functions
After taking the inputs, to run langchain models, 
use button with the appropriate button text`with this command

if st.button({button_text}):
    # rest of the code

Instruction:{instruction}
=============================
Streamlit Code:{streamlit_code}
=============================
LangChain Code:{langchain_code}
=============================
All imports:{imports_code_snippet}
=============================
Pipeline Explanation:{explanation}
=============================
Final Streamlit Code:
"""
