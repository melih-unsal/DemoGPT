from langchain_experimental.utilities import PythonREPL
from demogpt.tools import BaseTool

class PythonTool(BaseTool):
    def __init__(self):
        self.tool = PythonREPL()
        super().__init__()
        
    def run(self, code):
        return self.tool.run(code)
    
if __name__ == "__main__":
    tool = PythonTool()
    code = "print('Hello, World!')"
    print(tool.run(code))