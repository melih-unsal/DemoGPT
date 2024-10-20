from langchain_community.tools import YouTubeSearchTool as Youtube
from demogpt_agenthub.tools import BaseTool

class YouTubeSearchTool(BaseTool):
    def __init__(self):
        self.tool = Youtube()
        super().__init__()

    def run(self, query):
        return self.tool.run(query)
    
if __name__ == "__main__":
    query = "lex friedman"
    tool = YouTubeSearchTool()
    print(tool.run(query))