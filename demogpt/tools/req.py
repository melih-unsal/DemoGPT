from langchain_community.utilities import TextRequestsWrapper

class RequestUrlTool:
    def __init__(self):
        self.tool = TextRequestsWrapper()
        
    def run(self, url):
        return self.tool.get(url)
    
if __name__ == "__main__":
    tool = RequestUrlTool()
    print(tool.run("https://www.google.com"))