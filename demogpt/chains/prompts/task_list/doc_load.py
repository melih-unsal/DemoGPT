loaders = """
For Local TXT file:
TextLoader
################################
For Web Page:
WebBaseLoader
################################
For Online PDF:
OnlinePDFLoader
################################
For Local PDF:
UnstructuredPDFLoader
################################
For Power Point:
UnstructuredPowerPointLoader
################################
For CSV:
UnstructuredCSVLoader
################################
For Excel:
UnstructuredExcelLoader
"""

loader_dict = {
    "txt" : "TextLoader",
    "web_page" : "WebBaseLoader",
    "online_pdf" : "OnlinePDFLoader",
    "pdf" :"UnstructuredPDFLoader",
    "powerpoint" : "UnstructuredPowerPointLoader",
    "csv" : "UnstructuredCSVLoader",
    "excel" :"UnstructuredExcelLoader"
    }

system_template = f"""
Based on the provided context in 'Previous Code', choose the most appropriate loader.

These are your loader options:

{loaders}
"""

human_template = """
Use the information from 'Previous Code' to determine the loader from one of the 7 loader options.
Don't write any explanation but directly say the loader option

Instruction: {instruction}  
Previous Code: {code_snippets}
Loader Option:
"""
