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
CSVLoader
################################
For Excel:
UnstructuredExcelLoader
################################
For Docx:
UnstructuredWordDocumentLoader
################################
For Youtube:
YoutubeLoader
################################
For Notion Zip File:
NotionDirectoryLoader
"""

system_template = f"""
Based on the provided context in 'Previous Code', choose the most appropriate loader.

These are your loader options:

{loaders}
"""

human_template = """
Use the information from 'Previous Code' to determine the loader from one of the loader options.
Don't write any explanation but directly say the loader option

Instruction: {instruction}  
Previous Code: {code_snippets}
Loader Option:
"""
