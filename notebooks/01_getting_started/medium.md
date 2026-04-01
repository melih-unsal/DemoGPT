# How to Build AI Agents in Python with DemoGPT: A Step-by-Step Tutorial

## Why Building AI Agents Still Takes Too Long

You have an idea for an AI-powered application. Maybe it's a chatbot that answers questions from your company documents, or a research assistant that searches the web and performs calculations. With traditional frameworks, you're looking at hundreds of lines of boilerplate: setting up LangChain chains, wiring tool calls, managing prompts, building the UI layer.

**What if you could build a working AI agent in 5 lines of Python?** Or describe an app in plain English and get a complete Streamlit application generated automatically?

That's exactly what [DemoGPT](https://github.com/melih-unsal/DemoGPT) does. In this tutorial, you'll go from zero to a fully functional AI agent in under 10 minutes.

## What is DemoGPT? An Open-Source AI Agent Framework for Python

DemoGPT is an open-source Python framework with two core capabilities:

- **DemoGPT AgentHub** --- A modular toolkit for building AI agents with built-in tools (web search, code execution, Wikipedia, weather, and more), RAG (Retrieval Augmented Generation), and two agent types: `ToolCallingAgent` for single-step tasks and `ReactAgent` for multi-step reasoning.

- **DemoGPT Core** --- An automatic Streamlit app generator that converts natural language instructions into complete, runnable Python applications. Describe what you want; DemoGPT writes the code.

### How DemoGPT Compares to Other Frameworks

| Feature | DemoGPT | LangChain (raw) | AutoGen |
|---------|:-------:|:----------------:|:-------:|
| Built-in agent types | Yes | Manual setup | Yes |
| Tool ecosystem | 12+ tools included | Separate packages | Limited |
| RAG out of the box | Yes (Chroma, FAISS, Pinecone) | Manual setup | No |
| Auto app generation | Yes (Streamlit) | No | No |
| Lines of code for an agent | 5--10 | 30--50+ | 20--30 |

DemoGPT builds on top of LangChain internally but abstracts away the complexity, so you can focus on *what* your agent does rather than *how* it's wired together.

## Installation

```bash
pip install demogpt
```

This single command installs everything you need --- LangChain, OpenAI SDK, Tavily search, Chroma vector store, HuggingFace embeddings, and 12+ tool integrations.

Or install from source for the latest features:

```bash
git clone https://github.com/melih-unsal/DemoGPT.git
cd DemoGPT
pip install .
```

**Requirements:** Python 3.8+ and an OpenAI API key.

## Setting Up Your API Key

The recommended approach is using a `.env` file, which works reliably across terminals, Jupyter notebooks, and IDEs:

```
# .env file in your project root
OPENAI_API_KEY=sk-your-key-here
TAVILY_API_KEY=tvly-your-key-here
```

Then load it in Python:

```python
from dotenv import load_dotenv
load_dotenv()
```

`python-dotenv` is included with DemoGPT --- no extra install needed.

> You can get a free Tavily API key at [tavily.com](https://tavily.com). The free tier includes 1,000 searches per month.

## Tutorial: Build Your First AI Agent in Python

Let's create an agent that can search the web using Tavily and answer questions with up-to-date information:

```python
from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.tools import TavilySearchTool
from demogpt_agenthub.llms import OpenAIChatModel

# 1. Initialize the language model
llm = OpenAIChatModel(model_name="gpt-4o-mini")

# 2. Create a search tool
search_tool = TavilySearchTool()

# 3. Create an agent
agent = ToolCallingAgent(
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# 4. Run it
response = agent.run("What is DemoGPT?")
print(response)
```

That's it --- **5 lines of meaningful code** to build a web-searching AI agent.

With `verbose=True`, you'll see the agent's full reasoning chain:

```
Reasoning: The user wants to know about DemoGPT. I'll search the web.
Tool call: TavilySearch
Tool result: DemoGPT is an open-source framework for building AI agents...
Answer: DemoGPT is an open-source Python framework that...
```

## Using the LLM Directly (Without an Agent)

Sometimes you just need a simple LLM call without tools or agents:

```python
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")
response = llm.run("Explain what an AI agent is in 2 sentences.")
print(response)
```

DemoGPT supports all current OpenAI models including `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o`, `gpt-4o-mini`, and reasoning models like `o3` and `o4-mini`. You can also point it at self-hosted models via vLLM, Ollama, or any OpenAI-compatible endpoint using a custom `api_base` URL.

## Auto-Generate a Streamlit App from Natural Language

This is DemoGPT's standout feature. Describe the app you want in plain English, and DemoGPT generates the complete Streamlit code:

```python
from demogpt import DemoGPT

demo = DemoGPT(model_name="gpt-4o-mini")

instruction = "Create a simple app that takes a topic and generates a short poem about it"
title = "Poem Generator"

for phase in demo(instruction=instruction, title=title):
    print(f"Stage: {phase['stage']} | Progress: {phase['percentage']}%")
    if phase["done"]:
        print(phase["code"])  # Complete, runnable Streamlit app!
```

The generation pipeline has five stages:

1. **System Inputs** --- Detect required inputs (API keys, etc.)
2. **Plan** --- Create a structured execution plan
3. **Task** --- Break the plan into executable tasks (14 built-in task types)
4. **Draft** --- Generate Python code for each task
5. **Final** --- Assemble everything into a complete Streamlit application

Save the output to a file and run it:

```bash
streamlit run my_app.py
```

## DemoGPT Architecture at a Glance

DemoGPT AgentHub is organized into four modular layers:

| Module | What It Does |
|--------|-------------|
| `demogpt_agenthub.llms` | LLM wrappers --- OpenAI Chat and Text models with configurable temperature, max tokens, and custom API base |
| `demogpt_agenthub.tools` | 12+ built-in tools --- Tavily search, Wikipedia, arXiv, Python execution, Bash, weather, YOLO object detection, and more |
| `demogpt_agenthub.agents` | Two agent types --- `ToolCallingAgent` (single-step) and `ReactAgent` (multi-step ReAct reasoning) |
| `demogpt_agenthub.rag` | RAG pipeline --- Chroma, FAISS, and Pinecone vector stores with PDF, TXT, CSV, JSON, and URL ingestion |

Each module works independently or together. You can use just the LLM wrapper, or combine all four for a document-powered multi-step reasoning agent.

## What You Can Build with DemoGPT

- **Research assistants** that search the web, academic papers, and Wikipedia to synthesize answers
- **Document Q&A systems** using RAG with your PDFs, CSVs, or web content
- **Data analysis agents** that query documents and run Python calculations on the results
- **Customer support bots** powered by your knowledge base
- **Rapid prototypes** --- describe an app idea and get a working Streamlit app in minutes

## FAQ

**Is DemoGPT free?**
Yes. DemoGPT is open-source under the MIT License. You'll need an OpenAI API key (which has its own costs) and a Tavily API key for web search (free tier available at [tavily.com](https://tavily.com)).

**Does DemoGPT work with models other than OpenAI?**
Yes. You can use any OpenAI-compatible API by setting a custom `api_base` URL. This works with self-hosted models via vLLM, Ollama, or text-generation-inference.

**What's the difference between ToolCallingAgent and ReactAgent?**
`ToolCallingAgent` makes a single tool call per query --- fast and predictable. `ReactAgent` chains multiple tool calls with reasoning in between --- slower but capable of solving complex, multi-step tasks.

**Can I create custom tools?**
Absolutely. Extend the `BaseTool` class, implement a `run()` method, and pass it to any agent. We'll cover this in detail in Part 3 of this series.

## What's Next in This Series

This tutorial is Part 1 of a 7-part series covering every aspect of DemoGPT:

1. **Getting Started** --- You are here
2. **Language Models** --- Configuring LLMs, parameters, and custom endpoints
3. **Tools** --- All 12+ built-in tools and creating custom ones
4. **Tool Calling Agent** --- Single-step task execution in depth
5. **React Agent** --- Multi-step reasoning and tool chaining
6. **RAG** --- Document-powered AI with vector stores
7. **App Generation** --- Auto-generating Streamlit apps from natural language

Each article comes with a companion Jupyter notebook you can run yourself. All the code in this series has been tested and verified.

## Get Started Now

```bash
pip install demogpt
```

- [GitHub Repository](https://github.com/melih-unsal/DemoGPT) --- Star the project if you find it useful
- [Documentation](https://docs.demogpt.io) --- Full API reference
- [PyPI Package](https://pypi.org/project/demogpt/) --- Latest releases

DemoGPT turns the complexity of AI agent development into a few lines of Python. Whether you're prototyping an idea or building a production agent system, it gives you the tools to move fast without sacrificing flexibility.

---

*Tags: AI Agents, Python, LLM, OpenAI, Streamlit, RAG, Open Source, Tutorial, DemoGPT, LangChain*
