# Getting Started with DemoGPT: Build AI Agents and Apps in Minutes

## Introduction

The AI landscape is evolving rapidly, and building applications powered by large language models (LLMs) has become a critical skill. But what if you could generate entire LLM-powered applications from just a natural language description? Or build sophisticated AI agents with just a few lines of Python?

Enter **DemoGPT** --- an open-source framework that makes both of these possible.

In this article, we'll walk through what DemoGPT is, how to set it up, and how to build your first AI agent --- all in under 10 minutes.

## What is DemoGPT?

DemoGPT is a dual-purpose framework that combines two powerful capabilities:

1. **DemoGPT Core** --- Automatically generates complete Streamlit applications from natural language instructions. You describe what you want, and DemoGPT writes the code for you.

2. **DemoGPT AgentHub** --- A modular library for building, customizing, and managing AI agents equipped with tools, reasoning capabilities, and document retrieval (RAG).

Whether you're a developer looking to prototype quickly or a researcher exploring AI agent architectures, DemoGPT provides the tools you need.

## Installation

Getting started is as simple as:

```bash
pip install demogpt
```

Or if you want the latest features from source:

```bash
git clone https://github.com/melih-unsal/DemoGPT.git
cd DemoGPT
pip install .
```

## Setting Up Your API Key

DemoGPT uses OpenAI models under the hood. Set your API key:

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

## Your First AI Agent

Let's build a simple agent that can search the web. With DemoGPT AgentHub, this takes just a few lines:

```python
from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.tools import TavilySearchTool
from demogpt_agenthub.llms import OpenAIChatModel

# Initialize the language model
llm = OpenAIChatModel(model_name="gpt-4o-mini")

# Create a search tool
search_tool = TavilySearchTool()

# Create an agent with the search tool
agent = ToolCallingAgent(
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# Run the agent
response = agent.run("What is DemoGPT?")
print(response)
```

When you run this with `verbose=True`, you'll see the agent's entire thought process:
- **Reasoning**: Why it chose the search tool
- **Tool call**: The actual search query
- **Tool result**: What the search returned
- **Answer**: The synthesized response

## Using the LLM Directly

You can also use the language model without an agent:

```python
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")
response = llm.run("Explain what an AI agent is in 2 sentences.")
print(response)
```

## Generating a Streamlit App

Here's where DemoGPT truly shines. Describe the app you want, and DemoGPT generates the complete Streamlit code:

```python
from demogpt import DemoGPT

demo = DemoGPT(model_name="gpt-3.5-turbo")

instruction = "Create a simple app that takes a topic and generates a short poem about it"
title = "Poem Generator"

for phase in demo(instruction=instruction, title=title):
    print(f"Stage: {phase['stage']} | Progress: {phase['percentage']}%")
    if phase["done"]:
        print(phase["code"])
```

The generator yields progress through five stages:
1. **system_inputs** --- Detect required inputs
2. **plan** --- Create an execution plan
3. **task** --- Break the plan into tasks
4. **draft** --- Generate code snippets
5. **final** --- Assemble the complete app

## The DemoGPT Architecture

Under the hood, DemoGPT AgentHub is organized into four clean modules:

| Module | Purpose |
|--------|---------|
| `llms` | Language model wrappers (OpenAI Chat, OpenAI Text) |
| `tools` | 12+ built-in tools (search, weather, code execution, etc.) |
| `agents` | ToolCallingAgent (single-step) and ReactAgent (multi-step) |
| `rag` | Retrieval Augmented Generation with Chroma, FAISS, Pinecone |

Each module is designed to work independently or together, giving you flexibility in how you build your AI applications.

## What's Next?

This article barely scratches the surface. DemoGPT offers:

- **12+ built-in tools** including web search, Wikipedia, arXiv, weather, Python execution, and more
- **Custom tool creation** by extending the `BaseTool` class
- **ReactAgent** for multi-step reasoning with tool chaining
- **RAG** for document-powered question answering
- **Automatic app generation** from natural language

In the upcoming articles in this series, we'll deep-dive into each of these capabilities:

1. **Language Models** --- Configuring and using different LLMs
2. **Tools** --- Built-in tools and creating your own
3. **Tool Calling Agent** --- Single-turn task execution
4. **React Agent** --- Multi-step reasoning and planning
5. **RAG** --- Building document-powered AI systems
6. **App Generation** --- Creating complete Streamlit apps

## Conclusion

DemoGPT democratizes AI application development by providing both automated app generation and a flexible agent framework. Whether you need a quick prototype or a production-ready agent system, DemoGPT has you covered.

The project is open-source and actively maintained. Check it out on [GitHub](https://github.com/melih-unsal/DemoGPT) and give it a star if you find it useful!

---

*This article is part of a series on DemoGPT. Follow along to master every aspect of building AI agents and applications with this powerful framework.*
