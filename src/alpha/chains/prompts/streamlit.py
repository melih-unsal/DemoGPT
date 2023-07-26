human_template = """
Create an interactive Streamlit application
by applying the tasks in the Task List to accomplish the Instruction

When you call ai functions, please check if the inputs are non-empty before calling it
Make sure, that you don't use any function that you don't define.

After taking the inputs, to give the response, check inputs and trigger the system with the following code
```if st.button({button_text}):```

Task List:{task_list}
#################################
Instruction:{instruction}
#################################
AI Functions : {ai_functions}
Streamlit Code:
"""
