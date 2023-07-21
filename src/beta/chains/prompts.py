DOC_USE_TEMPLATE = """
As a Python developer, your task is to use the LangChain library to develop an application based on a user-provided idea.

If the document is useful, incorporate the information from it into your Python code for the application.

Document: {document}

Application Idea: {idea}

Proceed with your Python code below:
"""

INIT_GENERATION_TEMPLATE = """
As a Python developer, your task is to use the LangChain library to develop an llm-based application based on a user-provided idea. A document is provided to assist you, but it may or may not be relevant.

If you find the document irrelevant to the application idea, respond with "Not relevant". If the document is useful, incorporate the information from it into your Python code for the application.

Document: {document}

Application Idea: {idea}

Proceed with your Python code below:
"""

APP_GENERATION_TEMPLATE = """
As a Python developer, your task is to create a llm-based new application with the LangChain library based on a user-specified idea. 
Reference successful examples in the library's repository, translate the user's idea into specific requirements, draft an architecture, develop the application, and validate your work against the examples.mber, due to the one-shot nature of the task, attention to detail in understanding the examples, meticulous planning, and precise execution are paramount for successful application generation.

Possible answers:{possible_answers}

Application Idea:{idea}

LangChain Application Code:
"""

APP_DEBUGGING_TEMPLATE = """
As a software engineer, you are developing a Python application using the LangChain library. 
However, the current code is buggy and not functioning as expected. 
You have an application idea, the buggy code, and some feedback at your disposal. 
Analyze the buggy code in the context of the application idea, understand the issues based on the feedback received, propose necessary modifications, and implement the fixes to ensure the code aligns with the intended application idea.

Example Document:{document}
################################
Buggy Code:{draft_code}
################################
Application Idea:{idea}
################################
Feedback:{feedback}
################################
Refined Code:
"""

DIVIDE_TASKS_SYSTEM_TEMPLATE = """You are an AI assistant to create task.
"""

DIVIDE_TASKS_HUMAN_TEMPLATE = """
Think step by step.
First decide if the instruction consists of a single task.
if then directly return the task
Otherwise divide the instruction into chains of multiple subtasks

Instruction: Generate a system which can generate a song from song title and give a score to that song out of 10
Subinstructions: ["generate a song from song title", "generate score from a song out of 10"]

Instruction: Create a translation system that converts English to French
Subinstructions: ["Create a translation system that converts English to French"]

Instruction: Create a system that generates tweet from hashtags and given keywords
Subinstructions: ["Create a system that generates tweet from hashtags and given keywords"]

Instruction: System that generates blog from title then generate keywords for the blog post and translates the keywords from English to French
Subinstructions: ["generate a system that creates blog from title", "generate system that generates keywords from a blog post","generate system that translates keywords from English to French"]

Instruction: {task}
Subinstructions:
"""

MERGE_CODES_SYSTEM_TEMPLATE = """You are supposed to create a final code to accomplish final task 
by looking at the code block which are created to do the subtasks.
Please merge those codes to do the final task"""


MERGE_CODES_HUMAN_TEMPLATE = """
{examples}
Final Task: {task}
Final Code:
"""


STREAMLIT_CODE_SYSTEM_TEMPLATE = """
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. 
    You will get a GOAL.
    You will get a logic code that does the logic part of the GOAL
    Your task is generating a stremlit code to add a UI to the logic to accomplish the GOAL 
    When needed, you can use streamlit's session_state methodology like in the below:
    ################################################
    Initialize values in Session State
    The Session State API follows a field-based API, which is very similar to Python dictionaries:

    # Initialization
    if 'key' not in st.session_state:
        streamlit.session_state['key'] = 'value'
    
    # You can use streamlit.session_state['any_key'] to store your objects which is supposed to store state variables
    """

STREAMLIT_CODE_HUMAN_TEMPLATE = """Convert the logic code based on langchain library to an interactive streamlit appplication to accomplish the GOAL with the given title. 
Also when the final result is ready add st.balloons() to the code 
Keep in mind that if the streamlit code includes a list which will be updated during the application, 
use st.session_state because for each update, it needs to be stored. 
Otherwise, the object will be resetted. 
Don't define st.text_input inside of a while loop 
Don't forget to use all the "import" statements in langchain code
When memory related object is defined, please put it inside streamlit.session_state to preserve its content.


GOAL: {instruction}
--------- 
Langchain based Logic Code:
{langchain_code} 
---------
Streamlit Application Title: {title}
Add st.title({title}) to the app
---------
Interactive Stremlit Code:
"""

CODE_FEEDBACK_HUMAN_TEMPLATE = """
Is there any problem in the below code?
{code}
"""

CODE_REFINE_SYSTEM_TEMPLATE = """
    You are a helpful code assistant that refine a code according to the feedback, goal and the draft stremlit code. 
    You will get a GOAL.
    You will get a draft code
    You will get a feedback given to this code.
    Your task is refining the draft stremlit code to accomplish the GOAL according to the feedback
    """

CODE_REFINE_HUMAN_TEMPLATE = """
Keep in mind that if the streamlit code includes a list which will be updated during the application, 
use st.session_state because for each update, it needs to be stored. 
Otherwise, the object will be resetted. 
Don't define st.text_input inside of a while loop 
Don't forget to use all the "import" statements in langchain code

If the app is stateful, you can use streamlit's session_state methodology like in the below:
    ================================================================
    Initialize values in Session State
    The Session State API follows a field-based API, which is very similar to Python dictionaries:

    # Initialization
    if 'key' not in st.session_state:
        streamlit.session_state['key'] = 'value'
    
    # You can use streamlit.session_state['any_key'] to store your objects which is supposed to store state variables
    ================================================================

Remove the redundant parts of the draft streamlit code according to the goal and the feedback then refine the code

Goal: {instruction}
---------
Feedback: {feedback}
---------
Draft Stremlit Code: {code}
---------
Refined Code:
"""

CODE_REFINE1_HUMAN_TEMPLATE = """
Refine the code by fixing the bugs, 
removing redundant parts and transforming it into an interactive streamlit application code which gets input from the user.
################################################
Code:{code}
################################################
Refined Code:
"""
