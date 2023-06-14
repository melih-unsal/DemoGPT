
from PyPDF2 import PdfReader
from tqdm import tqdm, trange
import os

def convertToText(filepath,out_folder):
    """Converts pdf file to text

    Args:
        filepath (str): pdf file path

    Returns:
        str: txt format of pdf file
    """
    if not filepath.endswith('.pdf'):
        print("file must be a pdf file")
        return
    out_path = os.path.join(out_folder,filepath.split("/")[-1].replace(".pdf",".txt") ) 
    
    if os.path.exists(out_path):
        print("The corresponding txt file already exists")
        return
    reader = PdfReader(filepath)
    text = ""
    for i in trange(len(reader.pages)):
        page = reader.pages[i]
        text += page.extract_text()
    with open(out_path, "w") as f:
        f.write(text)
    print("Txt file has been created on",out_path)

def generateTxtFromFolder(src_folder,out_folder):
    os.makedirs(out_folder,exist_ok=True)
    for path in tqdm(os.listdir(src_folder)):
        full_path = os.path.join(src_folder,path)
        convertToText(full_path,out_folder)
