from langchain_community.tools.pubmed.tool import PubmedQueryRun

class PubmedTool:
    def __init__(self):
        self.tool = PubmedQueryRun()
    
    def run(self, query):
        return self.tool.invoke(query)

if __name__ == "__main__":
    tool = PubmedTool()
    print(tool.run("covid"))