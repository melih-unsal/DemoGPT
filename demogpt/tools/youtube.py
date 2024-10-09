from langchain_community.tools import YouTubeSearchTool as Youtube

class YouTubeSearchTool:
    def __init__(self):
        self.tool = Youtube()
    
    def run(self, query):
        return self.tool.run(query)
    
if __name__ == "__main__":
    query = "lex friedman"
    tool = YouTubeSearchTool()
    print(tool.run(query))