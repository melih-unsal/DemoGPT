from langchain_community.tools.pubmed.tool import PubmedQueryRun
from demogpt_agenthub.tools import BaseTool

class PubmedTool(BaseTool):
    def __init__(self):
        self.tool = PubmedQueryRun()
        super().__init__()
        
    def run(self, query):
        return self.tool.invoke(query)

if __name__ == "__main__":
    tool = PubmedTool()
    print(tool.run("covid"))