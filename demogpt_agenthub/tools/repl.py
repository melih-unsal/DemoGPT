from langchain_experimental.utilities import PythonREPL
from demogpt_agenthub.tools import BaseTool

class PythonTool(BaseTool):
    def __init__(self):
        self.tool = PythonREPL()
        super().__init__()
        self.name = "Python Interpreter"
        self.description = """A tool that can execute Python code to perform precise calculations by using the Python programming language. For any calculations that require a high degree of precision, this tool must be used.
        You must add print statement to the code to see the results of the calculations. Otherwise, the result will not be displayed."""
        
    def run(self, code):
        return self.tool.run(code)
    
if __name__ == "__main__":
    tool = PythonTool()
    code = "print('Hello, World!')"
    print(tool.run(code))