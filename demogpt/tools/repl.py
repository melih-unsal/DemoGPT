from langchain_experimental.utilities import PythonREPL

class PythonTool:
    def __init__(self):
        self.tool = PythonREPL()
        
    def run(self, code):
        return self.tool.run(code)
    
if __name__ == "__main__":
    tool = PythonTool()
    code = "print('Hello, World!')"
    print(tool.run(code))