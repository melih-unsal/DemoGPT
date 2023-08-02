system_template = """
Use the templates to guide the model in executing specific tasks or instructions. They act as directives, providing the context and structure needed for the model to respond appropriately.

Components:
1. "system_template": Describes the model's role and task for a given instruction. This string will be used with system_template.format(...) so only used curly braces for inputs
2. "template": Specifies the format for the model's response. This string will be used with template.format(...) so only used curly braces for inputs
3. "variety": Indicates how creative or deterministic the model's response should be.
4. "function_name": A unique identifier for the specific task or instruction.
5. "button_text": Text for a user interface button linked to the instruction, if applicable.

IMPORTANT NOTE:
- ONLY the variables listed under "Inputs" MUST be included in either the "system_template" or "template" section within curly braces (e.g., '{{variable_name}}'). Do NOT include any other parameters within curly braces.
- Ensure that the exact variable names listed in "Inputs" are used without any modifications.
- If a variable is listed in "Inputs," it must appear within curly braces in at least one of the "system_template" or "template" sections.
- "system_template" and "template" will be formatted with .format(inpu1=inpu1,inpu2=inpu2,...) so use all inputs in the combination of system_template and template.
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
"function_name": "blogger",
"button_text": "Generate Blog"
}}
##########################################
Instruction: Implement a language translation app.
Inputs: ["output_language", "text"]
Args: {{
"system_template": "You are a language translator. Your task is to translate text to {{output_language}}.",
"template": "Please translate the following text to {{output_language}}: '{{text}}'.",
"variety": "False",
"function_name": "translator",
"button_text": "Translate"
}}
##########################################
Instruction: Generate an appropriate name for an animal.
Inputs: ["animal"]
Args: {{
"system_template": "You are tasked with creating a name for an animal. You generate concise and fitting names.",
"template": "The animal is a {{animal}}. Please create a good name for it.",
"variety": "True",
"function_name": "animalNameGenerator",
"button_text": "Create Name"
}}
##########################################
Instruction: Create a programming-related humor machine.
Inputs: []
Args: {{
"system_template": "You are designed to generate humor related to programming. Be creative and entertaining.",
"template": "Please generate a programming-related joke or humorous statement.",
"variety": "True",
"function_name": "humorGenerator",
"button_text": "Generate Humor"
}}
##########################################
Instruction: Act as a math teacher to solve a problem.
Inputs: ["math_problem"]
Args: {{
"system_template": "You are a virtual math teacher, capable of solving any given math problem.",
"template": "The problem is: {{math_problem}}. Please solve it and show the steps.",
"variety": "False",
"function_name": "mathSolver",
"button_text": "Solve"
}}
##########################################
Instruction: Use AI to predict the user's horoscope based on analyzed traits.
Inputs: ["traits"]
Args: {{
"system_template": "You are skilled at predicting horoscopes based on analyzed traits and characteristics.",
"template": "The user has the following traits: {{traits}}. Please predict their horoscope based on this information.",
"variety": "False",
"function_name": "horoscopePredictor",
"button_text": "Predict Horoscope"
}}
##########################################
Instruction: Perform a scientific calculation.
Inputs: ["equation", "variables"]
Args: {{
"system_template": "You are a scientific calculator designed to solve equations with given variables.",
"template": "Solve the equation {{equation}} with the variables {{variables}}.",
"variety": "False",
"function_name": "scientificCalculator",
"button_text": "Calculate"
}}
##########################################
Instruction: Design a healthy meal plan.
Inputs: ["calories", "dietary_preferences"]
Args: {{
"system_template": "You are a nutritionist designing a healthy meal plan based on caloric needs and dietary preferences.",
"template": "Create a meal plan for {{calories}} calories per day, considering the following dietary preferences: {{dietary_preferences}}.",
"variety": "True",
"function_name": "mealPlanner",
"button_text": "Create Plan"
}}
##########################################
Instruction: Analyze a piece of artwork.
Inputs: ["artwork_description"]
Args: {{
"system_template": "You are an art critic tasked with analyzing and interpreting a piece of artwork.",
"template": "Based on the description: '{{artwork_description}}', please provide an analysis of the artwork.",
"variety": "True",
"function_name": "artCritic",
"button_text": "Analyze Artwork"
}}
##########################################
Instruction: Compose a piece of classical music.
Inputs: ["instrumentation", "theme"]
Args: {{
"system_template": "You are a composer creating a piece of classical music with specified instrumentation and theme.",
"template": "Compose a piece using the following instrumentation: {{instrumentation}}, based on the theme: '{{theme}}'.",
"variety": "True",
"function_name": "musicComposer",
"button_text": "Compose Music"
}}
##########################################
Instruction:{instruction}
Inputs:{inputs}
Args:(Use all {inputs} in the combination of system_template and template)
"""
