from demogpt.tools import BaseTool
class DuckDuckGoSearchTool(BaseTool):
    def __init__(self, raw_results=False, max_results=4, backend="text"):
        if raw_results:
            from langchain_community.tools import DuckDuckGoSearchResults
            self.tool = DuckDuckGoSearchResults(max_results=max_results, backend=backend)
        else:
            from langchain_community.tools import DuckDuckGoSearchRun
            self.tool = DuckDuckGoSearchRun()
        super().__init__()
        
    def run(self, inp):
        return self.tool.run(inp)
    
if __name__ == "__main__":
    query = "What is the capital of France?"
    raw_tool = DuckDuckGoSearchTool(raw_results=True, backend="news")
    print(raw_tool.run(query))
    tool = DuckDuckGoSearchTool()
    print(tool.run(query))
    
    