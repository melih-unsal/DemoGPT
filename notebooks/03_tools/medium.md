# DemoGPT Tools: Built-in Capabilities and Custom Tool Creation

## Introduction

Tools are what transform a language model from a text generator into a capable AI agent. DemoGPT AgentHub ships with 12+ built-in tools and provides a simple framework for creating your own.

In this article, we'll explore every built-in tool, understand the tool architecture, and learn how to create custom tools that extend your agent's capabilities.

## The Tool Architecture

Every tool in DemoGPT extends the `BaseTool` class:

```python
class BaseTool:
    name: str          # Tool identifier
    description: str   # What the tool does (agents read this!)

    def run(self, *args, **kwargs):
        raise NotImplementedError()
```

The `description` is crucial --- it's what agents use to decide which tool to call. A well-written description leads to better tool selection.

## Search & Information Tools

### TavilySearchTool

Powerful web search powered by Tavily (requires `TAVILY_API_KEY`):

```python
from demogpt_agenthub.tools import TavilySearchTool

tool = TavilySearchTool(max_results=5)
result = tool.run("latest advances in quantum computing")
print(result)
```

### WikipediaTool

Structured knowledge queries:

```python
from demogpt_agenthub.tools import WikipediaTool

tool = WikipediaTool()
result = tool.run("Artificial Intelligence")
print(result)
```

### ArxivTool

Academic paper search:

```python
from demogpt_agenthub.tools import ArxivTool

tool = ArxivTool()
result = tool.run("attention is all you need")
print(result)
```

### Other Search Tools

- **StackOverFlowTool** --- Programming Q&A
- **WikiDataTool** --- Structured data queries
- **PubmedTool** --- Medical and scientific literature
- **YouTubeSearchTool** --- Video search

## Data Processing Tools

### PythonTool

Execute Python code safely:

```python
from demogpt_agenthub.tools import PythonTool

tool = PythonTool()
result = tool.run("""
import math
numbers = [16, 25, 36, 49, 64]
roots = [math.sqrt(n) for n in numbers]
print(f"Square roots: {roots}")
print(f"Sum: {sum(roots):.2f}")
""")
print(result)
```

This is one of the most versatile tools --- agents can write and execute Python code to perform calculations, data processing, and more.

### BashTool

Execute shell commands:

```python
from demogpt_agenthub.tools import BashTool

tool = BashTool()
result = tool.run("echo 'Hello from DemoGPT!' && date")
print(result)
```

### RequestUrlTool

Fetch content from URLs:

```python
from demogpt_agenthub.tools import RequestUrlTool

tool = RequestUrlTool()
result = tool.run("https://httpbin.org/json")
print(result)
```

## Specialized Tools

### WeatherTool

Current weather data (requires `OPENWEATHERMAP_API_KEY`):

```python
from demogpt_agenthub.tools import WeatherTool

tool = WeatherTool()
result = tool.run("London")
print(result)
```

### YoloTool

Object detection in images:

```python
from demogpt_agenthub.tools import YoloTool

tool = YoloTool()
result = tool.run("https://ultralytics.com/images/bus.jpg")
print(result)  # "There are 1 bus, 4 persons in the image..."
```

## Creating Custom Tools

Creating a custom tool is straightforward. Extend `BaseTool` and implement `run()`:

```python
from demogpt_agenthub.tools import BaseTool

class CalculatorTool(BaseTool):
    def __init__(self):
        self.name = "CalculatorTool"
        self.description = (
            "Performs basic arithmetic calculations. "
            "Input should be a mathematical expression like '2 + 3' or '10 * 5'"
        )
        super().__init__()

    def run(self, expression: str):
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"

calc = CalculatorTool()
print(calc.run("25 * 4 + 10"))  # Output: 110
```

### A More Complex Example: Text Analyzer

```python
class TextAnalyzerTool(BaseTool):
    def __init__(self):
        self.name = "TextAnalyzer"
        self.description = (
            "Analyzes text and returns statistics including word count, "
            "character count, sentence count, and average word length."
        )
        super().__init__()

    def run(self, text: str):
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        avg_word_len = sum(len(w) for w in words) / len(words) if words else 0

        return (
            f"Words: {len(words)}, "
            f"Characters: {len(text)}, "
            f"Sentences: {sentences}, "
            f"Avg word length: {avg_word_len:.1f}"
        )
```

## Using Custom Tools with Agents

The magic happens when you give your custom tools to an agent:

```python
from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")

agent = ToolCallingAgent(
    tools=[CalculatorTool(), TextAnalyzerTool(), TavilySearchTool()],
    llm=llm,
    verbose=True
)

# The agent automatically picks the right tool
agent.run("Calculate 2^10 * 3")        # Uses CalculatorTool
agent.run("Analyze this text: ...")     # Uses TextAnalyzerTool
agent.run("What is quantum computing?") # Uses TavilySearchTool
```

## Best Practices for Custom Tools

1. **Write clear descriptions** --- The agent reads the description to decide when to use your tool. Be specific about inputs and capabilities.

2. **Handle errors gracefully** --- Return error messages as strings rather than raising exceptions. This lets the agent understand what went wrong.

3. **Keep tools focused** --- Each tool should do one thing well. Don't create a Swiss Army knife tool.

4. **Document input format** --- Include expected input format in the description (e.g., "Input format: '32F to C'").

5. **Return structured output** --- Consistent output formats help agents parse and use results effectively.

## Complete Tool Reference

| Tool | Module | API Key Required |
|------|--------|:---:|
| TavilySearchTool | `tools.tavily_search` | Yes |
| WikipediaTool | `tools.wikipedia` | No |
| ArxivTool | `tools.arxiv` | No |
| PythonTool | `tools.repl` | No |
| BashTool | `tools.bash` | No |
| RequestUrlTool | `tools.request_url` | No |
| WeatherTool | `tools.weather` | Yes |
| YouTubeSearchTool | `tools.youtube` | No |
| StackOverFlowTool | `tools.stackoverflow` | No |
| WikiDataTool | `tools.wikidata` | No |
| PubmedTool | `tools.pubmed` | No |
| YoloTool | `tools.yolo` | No |

## Conclusion

Tools are the interface between your AI agent and the real world. DemoGPT provides a rich set of built-in tools for common tasks and a simple framework for creating your own. By combining the right tools with the right agent, you can build AI systems that interact with the web, process data, execute code, and much more.

In the next article, we'll dive deep into the **ToolCallingAgent** and learn how it selects and uses tools to solve problems.

---

*This article is part of a series on DemoGPT. Check out the companion Jupyter notebook for hands-on examples.*
