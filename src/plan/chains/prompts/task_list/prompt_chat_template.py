system_template = """
Create system_template and template to help a model to generate an instruction.
The system_template and template will be used during the code generation to do the instruction.
You can think, these templates are kind of directives for the model to do the instruction.
So, it is good to create the templates in detail to direct the model.
variety becomes True when the model's response needs to various such as blog post generation.
variety becomes False when the model's response needs to strict such as translation or doing math operations.
"""

human_template = """
=========================================
Instruction:Generate blog post from title.
Inputs:[title]
Args: {{
"system_template":"You are a helpful assistant that generates a blog post from the title: {{title}}.",
"template":"Title is {{title}}",
"variety":"True",
"function_name":"blogger",
"button_text":"Generate Blog"
}}
##########################################
Instruction:Implement language translation app
Inputs:[input_language,output_language,text]
Args: {{
"system_template":"You are a helpful assistant that translates {{input_language}} to {{output_language}}.",
"template":"Translate {{text}}",
"variety":"False",
"function_name":"translator",
"button_text":"Translate"
}}
##########################################
Instruction:Generate animal name from animal
Inputs:[animal]
Args: {{
"system_template":"You are a helpful assistant that generates a name for an animal. You generate short answer.",
"template":"Create a good name for {{animal}}?",
"variety":"True",
"function_name":"animalNameGenerator",
"button_text":"Create Name"
}}
##########################################
Instruction:Create programming related humor machine
Inputs:[]
Args: {{
"system_template":"You are a helpful assistant that generates a humor related to programming.",
"template":"",
"variety":"True",
"function_name":"humorGenerator",
"button_text":"Generate Humor"
}}
##########################################
Instruction:Create a math teacher.
Inputs:[math_problem]
Args: {{
"system_template":"You are a helpful assistant that solve any math problem",
"template":"Here is the math problem you need to solve: {{math_problem}}",
"variety":"False",
"function_name":"mathSolver",
"button_text":"Solve"
}}
##########################################
Instruction:Use AI to predict the user's horoscope based on the analyzed traits and characteristics.
Inputs:[traits]
Args: {{
"system_template":"You are a helpful assistant that can predict the user's horoscope based on the analyzed traits and characteristics",
"template":"Here is the traits that the user has: {{traits}}.Now predict the user's horoscope based on this information",
"variety":"False",
"function_name":"mathSolver",
"button_text":"Solve"
}}
##########################################
Instruction:{instruction}
Inputs:{inputs}
Args:
"""
