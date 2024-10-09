from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

class WikipediaTool:
    def __init__(self):
        self.tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        
    def run(self, query):
        return self.tool.run(query)
    
if __name__ == "__main__":
    query = "How to create a list in python"
    tool = WikipediaTool()
    print(tool.run(query))