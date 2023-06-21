from bs4 import BeautifulSoup
import requests
from pprint import pprint
from tqdm import tqdm

with open("urls.txt", "r") as f:
    urls = f.readlines()

ROOT = "../documents/langchain/"

for site in tqdm(urls):
    site = site.strip().replace(".html","")  
    r = requests.get(site) 

    if r.status_code != 200:
        print(site)
        print("HTTP error")
        continue 
    # converting the text
    soup = BeautifulSoup(r.text,"html.parser")

    try:
        component = soup.find_all('div','theme-doc-markdown markdown')[0]
        header = component.find_all("h1")[0].get_text()
        text = component.get_text()
    except Exception as e:
        continue
    filepath = ROOT + header.replace("/","")+".txt"
    with open(filepath,"w") as f:
        f.write(text)
    
    
    