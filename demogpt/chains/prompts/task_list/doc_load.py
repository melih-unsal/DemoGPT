loaders = """
For Local TXT file:
from langchain.document_loaders import TextLoader
loader = TextLoader(<local_txt_file_path>)
################################
For Web Page:
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("<url>")
################################
For Online PDF:
from langchain.document_loaders import OnlinePDFLoader
loader = OnlinePDFLoader("<online_pdf_url>")
################################
For Local PDF:
from langchain.document_loaders import UnstructuredPDFLoader
loader = UnstructuredPDFLoader(
    <local_pdf_full_path>, mode="elements", strategy="fast"
    )
################################
For Power Point:
from langchain.document_loaders import UnstructuredPowerPointLoader
loader = UnstructuredPowerPointLoader(
    <local_powerpoint_file>, mode="elements", strategy="fast"
    )
################################
For CSV:
from langchain.document_loaders.csv_loader import UnstructuredCSVLoader
loader = UnstructuredCSVLoader(<csv_file_path>, mode="elements")
################################
For Excel:
from langchain.document_loaders.excel import UnstructuredExcelLoader
loader = UnstructuredExcelLoader(<excel_file_path>, mode="elements")
"""

system_template = f"""
These are the Loader classes that you should select.
Select the loader according to the input type unless the input type is ambiguous.
{loaders}
"""

human_template = """
Write a loader function using langchain.document_loaders 
to load the document for the argument name, variable and instruction 
below like in the below format:

###
def {function_name}({argument}):
    loader = Loader(path) # Select the appropriate Loader
    docs = loader.load()
    return docs

if {argument}:
    {variable} = {function_name}({argument})
else:
    {variable} = ''
###
    
While using the loader, don't change "mode" and "strategy" arguments, they need to be constant as stated.
If there are no such arguments, ignore it.

Instruction:{instruction}    

Document Loader Code:
"""
