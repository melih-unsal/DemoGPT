DOC_USE_TEMPLATE = """
As a Python developer, your task is to use the LangChain library to develop an application based on a user-provided idea.

If the document is useful, incorporate the information from it into your Python code for the application.

Document: {document}

Application Idea: {idea}

Proceed with your Python code below:
"""

INIT_GENERATION_TEMPLATE = """
As a Python developer, your task is to use the LangChain library to develop an application based on a user-provided idea. A document is provided to assist you, but it may or may not be relevant.

If you find the document irrelevant to the application idea, respond with "Not relevant". If the document is useful, incorporate the information from it into your Python code for the application.

Document: {document}

Application Idea: {idea}

Proceed with your Python code below:
"""

APP_GENERATION_TEMPLATE = """
As a Python developer, your task is to create a new application with the LangChain library based on a user-specified idea. 
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

DIVIDE_TASKS_TEMPLATE = """
Divide the instruction below to a couple of high level not detailed sub instructions 

Instruction: Generate a system which can generate a song from song title and give a score to that song out of 10
Instruction List: ["generate a song from song title", "generate score from a song out of 10"]

Instruction: Create a translation system that converts English to French
Instruction List: ["generate a English to French translator"]

Instruction :{task}
Instruction List: 
"""


MERGE_CODES_TEMPLATE = """
{examples}
Final Task: {task}
Final Code:
"""