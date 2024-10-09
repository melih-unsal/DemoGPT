from langchain_community.utilities import ArxivAPIWrapper

class ArxivTool:
    def __init__(self):
        self.tool = ArxivAPIWrapper()
        
    def run(self, query):
        return self.tool.run(query)
    
if __name__ == "__main__":
    tool = ArxivTool()
    print(tool.run("2106.01495"))