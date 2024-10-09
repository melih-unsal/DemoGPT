from langchain_community.utilities import StackExchangeAPIWrapper

class StackOverFlowTool:
    def __init__(self):
        self.tool = StackExchangeAPIWrapper()
    
    def run(self, query):
        return self.tool.run(query)
    
if __name__ == "__main__":
    query = "How to create a list in python"
    tool = StackOverFlowTool()
    print(tool.run(query))