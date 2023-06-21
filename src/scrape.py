from bs4 import BeautifulSoup
import requests
from time import time
   
# lists
urls=set()

start = time()
   
# function created
def scrape(site):

    if site in urls:
        return

    urls.add(site)
    print(site)
       
    # getting the request from url
    r = requests.get(site)
       
    # converting the text
    s = BeautifulSoup(r.text,"html.parser")
       
    for i in s.find_all("a"):
          
        href = i.attrs['href']
        
        if not href.startswith("/") or len(href) < 2 or site.endswith(href):
            continue
        index = site.find("/"+href.split("/")[1])
        if index > -1:
            subsection = site[:index] + href
        else:
            subsection = site + href           
        scrape(subsection)
            
scrape("https://python.langchain.com/docs/get_started")

end = time()

print("Processing time",int(end-start),"seconds")

print(len(urls),"urls are being written...")

with open("urls.txt","w") as f:
    for url in urls:
        f.write(url)
        f.write("\n")

