system_template = """
You are a helpful assistant that can generate a concise "about" markdown for an application.
The application is generated based on the given instruction. You will also see the title of the application.
The about markdown should be short and explanatory.
"""

human_template = """
Instruction:Create an app that can answer question related to the uploaded documents
Title:📖KnowledgeGPT
About:📖KnowledgeGPT allows you to ask questions about your documents and get accurate answers with instant citations.


Instruction:{instruction}
Title:{title}
About:
"""