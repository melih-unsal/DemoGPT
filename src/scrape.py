from bs4 import BeautifulSoup
import requests
   
# lists
urls=set()
   
# function created
def scrape(site):

    if site in urls:
        return

    urls.add(site)
       
    # getting the request from url
    r = requests.get(site)
       
    # converting the text
    s = BeautifulSoup(r.text,"html.parser")
       
    for i in s.find_all("a"):
          
        href = i.attrs['href'].replace("/docs/get_started","")
           
        if href.startswith("/") and len(href) > 1:              
            subsection = (site+href)
            print(subsection)
            scrape(subsection)
            
scrape("https://python.langchain.com/docs/get_started")