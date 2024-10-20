# 🚀 DemoGPT AgentHub

Welcome to DemoGPT AgentHub! This powerful library allows you to create, customize, and use AI agents with various tools. Let's dive in and explore how you can leverage this amazing library! 🎉

## 📚 Table of Contents

- [Installation](#-installation)
- [Creating Tools](#-creating-tools)
- [Available Tools](#-available-tools)
- [Initializing an Agent](#-initializing-an-agent)
- [Using an Agent](#-using-an-agent)
- [Available Agent Types](#-available-agent-types)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠 Installation

To install DemoGPT AgentHub, simply run:

```bash 
pip install demogpt
```


## 🔧 Creating Tools

Creating custom tools is easy! Here's how you can create your own tool:

1. Inherit from the `BaseTool` class
2. Implement the `run` method
3. Set the `name` and `description` attributes

Here's an example:

```python
from demogpt_agenthub.tools import BaseTool
class MyCustomTool(BaseTool):
    def __init__(self):
        self.name = "MyCustomTool"
        self.description = "This tool does something amazing!"
        super().__init__()
    def run(self, query):
        # Implement your tool's functionality here
        return f"Result for: {query}"
```

## 🧰 Available Tools

DemoGPT AgentHub comes with several built-in tools:

- 🔍 DuckDuckGoSearchTool
- 🌦 WeatherTool
- 📚 WikipediaTool
- 🐚 BashTool
- 🐍 PythonTool
- 📄 ArxivTool
- 🎥 YouTubeSearchTool
- 💻 StackOverFlowTool
- 🌐 RequestUrlTool
- 🗃 WikiDataTool
- 🏥 PubmedTool

## 🤖 Initializing an Agent

To create an agent, you'll need to:

1. Import the desired agent type
2. Initialize the tools you want to use
3. Create an instance of the agent with the tools and LLM

Here's an example:

```python
from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.llms import OpenAIChatModel
from demogpt_agenthub.tools import DuckDuckGoSearchTool, WeatherTool
search_tool = DuckDuckGoSearchTool()
weather_tool = WeatherTool()
llm = OpenAIChatModel(model_name="gpt-4o-mini")
agent = ToolCallingAgent(tools=[search_tool, weather_tool], llm=llm, verbose=True)
```


## 🎮 Using an Agent

Once you've created an agent, you can use it to ask questions or perform tasks:

```python
query = "What's the weather like in New York today?"
response = agent.ask(query)
print(response)
```


## 👥 Available Agent Types

Currently, DemoGPT AgentHub supports the following agent types:

1. 🛠 ToolCallingAgent: An agent that can use multiple tools to answer questions and perform tasks.

More agent types will be added in future updates!

## 🤝 Contributing

We welcome contributions to DemoGPT AgentHub! If you have ideas for new features, tools, or improvements, please open an issue or submit a pull request.

## 📄 License

DemoGPT AgentHub is released under the MIT License. See the LICENSE file for more details.
