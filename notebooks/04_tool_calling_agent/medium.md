# ToolCallingAgent in DemoGPT: Building Single-Step AI Agents

## Introduction

Not every AI task requires complex multi-step reasoning. Many practical problems can be solved with a single, well-chosen tool call. That's exactly what DemoGPT's `ToolCallingAgent` is designed for --- fast, efficient, single-step task execution.

In this article, we'll explore how the ToolCallingAgent works, when to use it, and how to build effective single-step agents.

## How ToolCallingAgent Works

The ToolCallingAgent follows a straightforward flow:

```
Query -> Reasoning -> Tool Selection -> Tool Execution -> Answer Synthesis
```

1. **Receives a query** from the user
2. **Reasons** about which tool is most appropriate
3. **Calls the selected tool** with the right parameters
4. **Synthesizes** the tool's output into a coherent answer

Unlike the ReactAgent, it makes exactly **one tool call** per query, making it faster and more predictable.

## Basic Example: Web Search Agent

```python
from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.tools import TavilySearchTool
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")
search = TavilySearchTool()

agent = ToolCallingAgent(
    tools=[search],
    llm=llm,
    verbose=True
)

response = agent.run("What are the latest developments in quantum computing?")
```

With `verbose=True`, you'll see the full reasoning chain:

```
Reasoning: The user wants current information about quantum computing.
           I'll use TavilySearchTool to find the latest news.
Tool call: TavilySearchTool
Tool result: [search results...]
Answer: Based on recent developments...
```

## Multi-Tool Selection

The real power of ToolCallingAgent emerges when you give it multiple tools:

```python
from demogpt_agenthub.tools import (
    TavilySearchTool,
    WikipediaTool,
    PythonTool
)

agent = ToolCallingAgent(
    tools=[TavilySearchTool(), WikipediaTool(), PythonTool()],
    llm=llm,
    verbose=True
)

# The agent picks the right tool for each query
agent.run("Calculate the factorial of 12")  # -> PythonTool
agent.run("Tell me about Albert Einstein")  # -> WikipediaTool
agent.run("Latest SpaceX launch news")      # -> TavilySearchTool
```

The agent reads each tool's `description` attribute and matches it against the query to select the best tool.

## Verbose vs Silent Mode

**Verbose mode** (`verbose=True`) is invaluable during development:

```python
# Development: see the reasoning
agent = ToolCallingAgent(tools=tools, llm=llm, verbose=True)

# Production: clean output only
agent = ToolCallingAgent(tools=tools, llm=llm, verbose=False)
```

Verbose output includes color-coded sections:
- **Reasoning** (blue) --- Why the agent chose a specific tool
- **Tool call** (yellow) --- Which tool was selected
- **Tool result** (cyan) --- The raw output from the tool
- **Answer** (green) --- The final synthesized response

## Building Custom Tools for the Agent

You can create specialized tools and use them with the ToolCallingAgent:

```python
from demogpt_agenthub.tools import BaseTool

class UnitConverterTool(BaseTool):
    def __init__(self):
        self.name = "UnitConverter"
        self.description = (
            "Converts temperatures between Celsius and Fahrenheit. "
            "Input format: '32F to C' or '100C to F'"
        )
        super().__init__()

    def run(self, query: str):
        query = query.strip().upper()
        if "F TO C" in query:
            f = float(query.split("F")[0])
            return f"{(f - 32) * 5/9:.2f} Celsius"
        elif "C TO F" in query:
            c = float(query.split("C")[0])
            return f"{c * 9/5 + 32:.2f} Fahrenheit"
        return "Invalid format. Use '32F to C' or '100C to F'"

agent = ToolCallingAgent(
    tools=[UnitConverterTool(), TavilySearchTool()],
    llm=llm,
    verbose=True
)

response = agent.run("Convert 98.6 Fahrenheit to Celsius")
print(response)
```

## ToolCallingAgent vs ReactAgent: When to Use Which

| Feature | ToolCallingAgent | ReactAgent |
|---------|:---:|:---:|
| Tool calls per query | 1 | Multiple |
| Speed | Fast | Slower |
| Complexity | Simple tasks | Complex reasoning |
| Predictability | High | Variable |
| Cost (tokens) | Low | Higher |

**Use ToolCallingAgent when:**
- The task can be solved with a single tool call
- Speed and cost matter
- You want predictable behavior
- Examples: search, calculation, data lookup

**Use ReactAgent when:**
- The task requires multiple steps
- Information from one tool informs the next action
- Complex reasoning is needed
- Examples: research + calculation, multi-source analysis

## Real-World Use Cases

### Customer Support Agent
```python
class FAQTool(BaseTool):
    def __init__(self, faqs):
        self.name = "FAQSearch"
        self.description = "Searches the FAQ database for answers to customer questions"
        self.faqs = faqs
        super().__init__()

    def run(self, query):
        # Simple keyword matching (use RAG for production)
        for q, a in self.faqs.items():
            if any(word in query.lower() for word in q.lower().split()):
                return a
        return "I couldn't find an answer. Please contact support."

faqs = {
    "return policy": "You can return items within 30 days.",
    "shipping time": "Standard shipping takes 3-5 business days.",
    "payment methods": "We accept credit cards, PayPal, and Apple Pay."
}

agent = ToolCallingAgent(
    tools=[FAQTool(faqs)],
    llm=llm,
    verbose=True
)
```

### Code Helper Agent
```python
agent = ToolCallingAgent(
    tools=[PythonTool(), StackOverFlowTool()],
    llm=llm,
    verbose=True
)

agent.run("Write a Python function to check if a number is prime")
```

## Best Practices

1. **Limit tools to 5-7** --- Too many tools can confuse the selection process.

2. **Write distinct descriptions** --- Make sure tool descriptions don't overlap, so the agent can clearly distinguish between them.

3. **Use verbose mode for debugging** --- Always develop with `verbose=True` to understand tool selection decisions.

4. **Handle tool failures gracefully** --- Ensure your tools return error messages as strings rather than raising exceptions.

5. **Start simple, upgrade if needed** --- Try ToolCallingAgent first. Only switch to ReactAgent if you genuinely need multi-step reasoning.

## Conclusion

The ToolCallingAgent is DemoGPT's workhorse for straightforward AI tasks. Its single-step architecture makes it fast, predictable, and cost-effective. By combining it with the right set of tools --- built-in or custom --- you can build powerful AI agents that handle search, computation, data lookup, and more.

In the next article, we'll explore the **ReactAgent**, which takes things to the next level with multi-step reasoning and tool chaining.

---

*This article is part of a series on DemoGPT. Check out the companion Jupyter notebook for hands-on examples.*
