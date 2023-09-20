system_template = """
Generate a prompt to guide the model in executing specific role. It acts as directives, providing the context and structure needed for the model to respond appropriately.

Components:
1. "system_template": Describes the model's role and task for a given instruction. This string will be used with system_template.format(...) so only used curly braces for inputs
2. "variety": Indicates how creative or deterministic the model's response should be.
3. "function_name": A unique identifier for the specific task or instruction.

IMPORTANT NOTE:
- Write "system_template" in a way that, system_template.format(input=something for input in inputs) work.
It should also have {{chat_history}}
What I mean is that, put all the elements of Inputs inside of system_template with curly braces so that I can format it with predefined parameters.
"""

human_template = """
IMPORTANT NOTE:
- ONLY the variables listed under "Inputs" MUST be included in either the "system_template" section within curly braces (e.g., '{{variable_name}}'). Do NOT include any other parameters within curly braces.
- Ensure that the exact variable names listed in "Inputs" are used without any modifications.
- If a variable is listed in "Inputs," it must appear within curly braces in the "system_template".
=========================================
Instruction: Generate a blog post from a title.
Inputs: ["human_input","title"]
Args: {{
"system_template":"
You are a chatbot having a conversation with a human. You are supposed to write a blog post from given title. Human want you to generate a blog post but you are also open to feedback and according to the given feedback, you can refine the blog \n\nTitle:{{title}}\n\n{{chat_history}}\nHuman: {{human_input}}\nBlogger:",
"variety": "True",
"function_name": "chat_blogger"
}}
##########################################
Instruction: Talk like a psychologist with a given tone.
Inputs: ["talk_input","tone"]
Args: {{
"system_template": "You are a psychologist. Reply to your patience with the given tone\n\nTone:{{tone}}\n\n{{chat_history}}\nPatience: {{talk_input}}\nPsychologist:",
"variety": "False",
"function_name": "talk_like_a_psychologist"
}}
##########################################
Instruction: Answer question related to the uploaded powerpoint file.
Inputs: ["question","powerpoint_doc"]
Args: {{
"system_template": "You are a chatbot having a conversation with a human.\n\nGiven the following extracted parts of a long document, chat history and a question, create a final answer.\n\n{{powerpoint_doc}}\n\n{{chat_history}}\nHuman: {{question}}\nChatbot:",
"variety": "False",
"function_name": "talk_like_a_psychologist"
}}
##########################################
Instruction: Talk like a mathematician
Inputs: ["human_input"]
Args: {{
"system_template": "You are a mathematician. Solve the human's mathematics problem as efficient as possible.\n\n{{chat_history}}\nHuman: {{human_input}}\nMathematician:",
"variety": "True",
"function_name": "solveMathProblem"
}}
##########################################
Instruction:{instruction}
Inputs:{inputs}
Args:
"""
