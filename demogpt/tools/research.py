from langchain_community.utilities import ArxivAPIWrapper
from demogpt.tools import BaseTool

class ArxivTool(BaseTool):
    def __init__(self):
        self.tool = ArxivAPIWrapper()
        super().__init__()

    def run(self, query):
        return self.tool.run(query)
    
if __name__ == "__main__":
    tool = ArxivTool()
    print(tool.run("2106.01495"))