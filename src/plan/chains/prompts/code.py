system_template = """
Create system_template and template to help a model to generate an instruction.
The system_template and template will be used during the code generation to do the instruction.
You can think, these templates are kind of directives for the model to do the instruction.
So, it is good to create the templates in detail
"""

human_template = """
=========================================
Instruction:Generate blog post from title.
Inputs:[title]
Args: {{
"system_template":"You are a helpful assistant that generates a blog post from the title: {{title}}.",
"template":"Title is {{title}}",
"examples":"",
"variety":"True"
}}
##########################################
Instruction:Implement language translation app
Inputs:[input_language,output_language,text]
Args: {{
"system_template":"You are a helpful assistant that translates {{input_language}} to {{output_language}}.",
"template":"Translate {{text}}",
"examples":"",
"variety":"False"
}}
##########################################
Instruction:Generate animal name from animal
Inputs:[animal]
Args: {{
"system_template":"You are a helpful assistant that generates a name for an animal. You generate short answer.",
"template":"Create a good name for {{animal}}?",
"examples":"Create a good name for cat\nFelix\nCreate a good name for horse\nSugar\n"
"variety":"True"
}}
##########################################
Instruction:Create programming related humor machine
Inputs:[]
Args: {{
"system_template":"You are a helpful assistant that generates a humor related to programming.",
"template":"",
"examples":"",
"variety":"True"
}}
##########################################
Instruction:Create a math teacher.
Inputs:[math_problem]
Args: {{
"system_template":"You are a helpful assistant that solve any math problem",
"template":"Here is the math problem: {{math_problem}}",
"examples":"",
"variety":"False"
}}
##########################################
Instruction:{instruction}
Inputs:{inputs}
Args:
"""
