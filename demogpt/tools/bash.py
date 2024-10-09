from langchain_community.tools import ShellTool

class BashTool:
    def __init__(self):
        self.tool = ShellTool()
    
    def run(self, commands):
        if isinstance(commands, str):
            return self.tool.run(({"commands": [commands]}))
        return self.tool.run(({"commands": commands}))
    
if __name__ == "__main__":
    commands = ["ls", "pwd"]
    tool = BashTool()
    print(tool.run(commands))
    command = "ls"
    print(tool.run(command))