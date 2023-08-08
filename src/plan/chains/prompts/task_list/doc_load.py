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
You will summarization code with a strict structure like in the below but 
loader will change depending on the input
###
def getDoc(argument):
    loader = Loader(path) # it changes depending on the path
    return loader.load()
if argument:
    variable = summarize(argument)
else:
    out_variable = ""
###

These are the Loader classes that you should select dependent on the url

{loaders}
"""

human_template = """
Write a loader function to load the document for the argument name, variable and instruction below:
Instruction:{instruction}
Argument Name : {argument}
Variable Name : {variable}
Summarization Code:
"""