system_template = """
Use the templates to guide the model in executing specific tasks or instructions. They act as directives, providing the context and structure needed for the model to respond appropriately.

Components:
1. "system_template": Describes the model's role and task for a given instruction. This string will be used with system_template.format(...) so only used curly braces for inputs
2. "template": Specifies the format for the model's response. This string will be used with template.format(...) so only used curly braces for inputs
3. "variety": Indicates how creative or deterministic the model's response should be.
4. "function_name": A unique identifier for the specific task or instruction.

IMPORTANT NOTE:
- Write "system_template" and "template" in a way that, (system_template+template).format(input=something for input in inputs) work.
What I mean is that, put all the elements of Inputs inside of either template or system_template with curly braces so that I can format it with predefined parameters.
"""

human_template = """
IMPORTANT NOTE:
- ONLY the variables listed under "Inputs" MUST be included in either the "system_template" or "template" section within curly braces (e.g., '{{variable_name}}'). Do NOT include any other parameters within curly braces.
- Ensure that the exact variable names listed in "Inputs" are used without any modifications.
- If a variable is listed in "Inputs," it must appear within curly braces in at least one of the "system_template" or "template" sections.
=========================================
Instruction: Generate a blog post from a title.
Inputs: ["title"]
Args: {{
"system_template": "You are an assistant designed to write a blog post from the given title: '{{title}}'.",
"template": "Title: {{title}}. Please compose a blog post based on this title.",
"variety": "True",
"function_name": "blogger"
}}
##########################################
Instruction: Implement a language translation app from one language to another.
Inputs: ["source_language","output_language", "text"]
Args: {{
"system_template": "You are a language translator. Your task is to translate text from {{source_language}} to {{output_language}}.",
"template": "Please translate the following text to {{output_language}}: '{{text}}'.",
"variety": "False",
"function_name": "translator"
}}
##########################################
Instruction: Generate an appropriate name for an animal.
Inputs: ["animal"]
Args: {{
"system_template": "You are tasked with creating a name for an animal. You generate concise and fitting names.",
"template": "The animal is a {{animal}}. Please create a good name for it.",
"variety": "True",
"function_name": "animalNameGenerator"
}}
##########################################
Instruction: Create a programming-related humor machine.
Inputs: []
Args: {{
"system_template": "You are designed to generate humor related to programming. Be creative and entertaining.",
"template": "Please generate a programming-related joke or humorous statement.",
"variety": "True",
"function_name": "humorGenerator"
}}
##########################################
Instruction: Act as a math teacher to solve a problem.
Inputs: ["math_problem"]
Args: {{
"system_template": "You are a virtual math teacher, capable of solving any given math problem.",
"template": "The problem is: {{math_problem}}. Please solve it and show the steps.",
"variety": "False",
"function_name": "mathSolver"
}}
##########################################
Instruction: Compose a piece of classical music.
Inputs: ["instrumentation", "theme"]
Args: {{
"system_template": "You are a composer creating a piece of classical music with specified instrumentation and theme.",
"template": "Compose a piece using the following instrumentation: {{instrumentation}}, based on the theme: '{{theme}}'.",
"variety": "True",
"function_name": "musicComposer"
}}
##########################################
Instruction:{instruction}
Inputs:{inputs}
Args:
"""
