# 🤖 From Demo to Product: The All-in-One Agent Library

<p align="center">
<a href=""><img src="assets/banner_small.png" alt="DemoGPT logo: Generate automatic LangChain pipelines" width="450px"></a>
</p>

<p align="center">
<b>⚡ Everything you need to create an LLM Agent is here. Access a comprehensive suite of tools, prompts, frameworks, and a knowledge hub of LLM models—all in one place to streamline your agent development.</b>
</p>

<p align="center">
<a href="https://pepy.tech/project/demogpt"><img src="https://static.pepy.tech/badge/demogpt" alt="Downloads"></a>
<a href="https://github.com/melih-unsal/DemoGPT/releases"><img src="https://img.shields.io/github/release/melih-unsal/DemoGPT" alt="Releases"></a>
<a href="https://demogpt.io"><img src="https://img.shields.io/badge/Official%20Website-demogpt.io-blue?style=flat&logo=world&logoColor=white" alt="Official Website"></a>
<a href="https://docs.demogpt.io"><img src="https://img.shields.io/badge/Documentation-📘-blueviolet" alt="DemoGPT Documentation"></a>
</p>

<p align="center">
<a href="docs/README_CN.md"><img src="https://img.shields.io/badge/文档-中文版-blue.svg" alt="CN doc"></a>
<a href="README.md"><img src="https://img.shields.io/badge/document-English-blue.svg" alt="EN doc"></a>
<a href="docs/ROADMAP_CN.md"><img src="https://img.shields.io/badge/ROADMAP-路线图-blue" alt="roadmap"></a>
<a href="docs/ROADMAP.md"><img src="https://img.shields.io/badge/ROADMAP-english-red" alt="roadmap"></a>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

<p align="center">
<a href="https://github.com/melih-unsal/DemoGPT/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues/melih-unsal/DemoGPT.svg?maxAge=2592000000000000" alt="Open an issue"></a>
<a href="https://github.com/melih-unsal/DemoGPT/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/melih-unsal/DemoGPT.svg?maxAge=25920000000000000000" alt="Closed issues"></a>
<a href="https://star-history.com/#melih-unsal/DemoGPT"><img src="https://img.shields.io/github/stars/melih-unsal/DemoGPT?style=social" alt="DemoGPT  Stars"></a>
<a href=""><img src="https://img.shields.io/github/forks/melih-unsal/DemoGPT" /> </a>
</p>

<p align="center">
<a href="https://twitter.com/demo_gpt"><img src="https://img.shields.io/twitter/follow/demo_gpt?style=social" alt="Twitter Follow"></a>
<a href="https://demogpt.medium.com/"><img src="https://img.shields.io/static/v1?style=for-the-badge&message=Medium&color=000000&logo=Medium&logoColor=FFFFFF&label=" alt="DemoGPT Medium" height="20"/></a>
<a href="https://www.producthunt.com/posts/demogpt?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-demogpt" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=406106&theme=light" alt="DemoGPT - Auto&#0032;generative&#0032;AI&#0032;app&#0032;generator&#0032;with&#0032;the&#0032;power&#0032;of&#0032;Llama&#0032;2 | Product Hunt" height="20" /></a>
</p>

<p align="center">
<a href="https://demogpt.streamlit.app"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit application"></a>
<a href="https://huggingface.co/spaces/melihunsal/demogpt"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Spaces-yellow"></a>
</p>

## 📑 Table of Contents

- [Introduction](#-introduction)
- [Architecture](#️-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Package Version](#-for-the-package-version)
  - [Python Interface](#-for-the-python-interface)
  - [Source Code Version](#-for-the-source-code-version)
- [DemoGPT AgentHub](#-demogpt-agenthub)
  - [Installation](#-installation-1)
  - [Creating Tools](#-creating-tools)
  - [Available Tools](#-available-tools)
  - [Creating an Agent](#-creating-an-agent)
  - [Using an Agent](#-using-an-agent)
  - [Available Agent Types](#-available-agent-types)
  - [Using ReactAgent](#-using-reactagent)
  - [Using RAG](#-using-rag)
- [To-Do](#to-do-)
- [Contribute](#-contribute)
- [Citations](#-citations)
- [License](#-license)

## 🤖 DemoGPT AgentHub

DemoGPT AgentHub is a powerful library that allows you to create, customize, and use AI agents with various tools.

### 🛠 Installation

To use DemoGPT AgentHub, simply install the main package:

```bash 
pip install demogpt
```

### 🔧 Creating Tools

Creating custom tools is easy:

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

### 🧰 Available Tools

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

### 🤖 Creating an Agent

To create an agent:

```python
from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.llms import OpenAIChatModel
from demogpt_agenthub.tools import DuckDuckGoSearchTool, WeatherTool

search_tool = DuckDuckGoSearchTool()
weather_tool = WeatherTool()
llm = OpenAIChatModel(model_name="gpt-4o-mini")
agent = ToolCallingAgent(tools=[search_tool, weather_tool], llm=llm, verbose=True)
```

### 🎮 Using an Agent

Once you've created an agent, use it to ask questions or perform tasks:

```python
query = "What's the weather like in New York today?"
response = agent.run(query)
print(response)
```

### 👥 Available Agent Types

Currently, DemoGPT AgentHub supports:

- 🛠 ToolCallingAgent: An agent that can use multiple tools to answer questions and perform tasks.
- 🔄 ReactAgent: An agent that shows its reasoning process, makes decisions, and uses tools step-by-step.

### 🧠 Using ReactAgent

The ReactAgent provides a detailed reasoning process:

```python
from demogpt_agenthub.tools import DuckDuckGoSearchTool, WeatherTool, PythonTool
from demogpt_agenthub.llms import OpenAIChatModel
from demogpt_agenthub.agents import ReactAgent

search_tool = DuckDuckGoSearchTool()
weather_tool = WeatherTool()
python_tool = PythonTool()

agent = ReactAgent(
    tools=[search_tool, weather_tool, python_tool],
    llm=OpenAIChatModel(model_name="gpt-4o-mini"),
    verbose=True
)

query = "What is the weather's temperature's square root in the country where Cristiano Ronaldo is currently playing?"
print(agent.run(query))
```

### 🧮 Using RAG

BaseRAG provides an easy way to implement Retrieval Augmented Generation with various vector stores:

```python
from demogpt_agenthub.rag import BaseRAG
from demogpt_agenthub.llms import OpenAIChatModel

# Initialize RAG system
rag = BaseRAG(
    llm=OpenAIChatModel(model_name="gpt-4o-mini"), 
    vectorstore="chroma",  # Supports "chroma", "pinecone", "faiss"
    persistent_path="rag_chroma",  # Where to store the vector database
    index_name="rag_index",
    reset_vectorstore=True,  # Whether to reset existing vectorstore
    embedding_model_name="sentence-transformers/all-mpnet-base-v2",  # Or use OpenAI models
    filter={"search_kwargs": {"score_threshold": 0.5}}
)

# Add documents
rag.add_files(["path/to/your/document.pdf"])  # Supports PDF, TXT, CSV, JSON
# Or add raw text
rag.add_texts(["Your text content here"])

# Query the RAG system
response = rag.run("What information can you find about X?")
```

Features:
- 📚 Multiple vectorstore support (Chroma, Pinecone, FAISS)
- 🔤 Multiple embedding model options:
  - Sentence Transformers (e.g., "sentence-transformers/all-mpnet-base-v2")
  - OpenAI Embeddings ("text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002")
- 📄 Multiple file format support:
  - PDF files
  - Text files
  - CSV files
  - JSON files
  - Web pages (via URLs)
- 💾 Persistent storage with automatic connection management
- 🔍 Configurable similarity search with filters and thresholds

Example use cases:

```python
# Example 1: Create a RAG system for a PDF document
rag = BaseRAG(
    llm=OpenAIChatModel(model_name="gpt-4o-mini"),
    vectorstore="chroma",
    persistent_path="rag_chroma",
    index_name="rag_index",
    reset_vectorstore=True
)
rag.add_files(["document.pdf"])
answer = rag.run("What are the key points in the document?")

# Example 2: Create a RAG system with web content
rag = BaseRAG(
    llm=OpenAIChatModel(model_name="gpt-4o-mini"),
    vectorstore="chroma",
    persistent_path="web_content",
    index_name="web_index"
)
rag.add_files(["https://example.com/article"])
answer = rag.run("Summarize the web content")
```

## 🔥 Demo


![Tweet Generator](assets/web_blogger.gif)

## 📚 Documentation

See our documentation site [here](https://docs.demogpt.io/) for full how-to docs and guidelines

⚡ With DemoGPT v1.3, API usage will be possible with the power of **Gorilla** within 2 weeks.
After this release, you will be able use external APIs autonomously. ⚡

## 📦 Using DemoGPT Package

The DemoGPT package is now available and can be installed using pip. Run the following command to install the package:

```sh
pip install demogpt
```

To use the DemoGPT application, simply type "demogpt" into your terminal:

```sh
demogpt
```


## 📌 Introduction

Welcome to DemoGPT, a revolutionary open-source initiative that is reshaping the landscape of Large Language Model (LLM) based application development.

At the heart of DemoGPT, the capabilities of GPT-3.5-turbo come to life, driving the automatic generation of LangChain code. This process is enriched with a sophisticated architecture that translates user instructions into interactive Streamlit applications.

### How DemoGPT Works

1. **Planning:** DemoGPT starts by generating a plan from the user's instruction.
2. **Task Creation:** It then creates specific tasks from the plan and instruction.
3. **Code Snippet Generation:** These tasks are transferred into code snippets.
4. **Final Code Assembly:** The code snippets are combined into a final code, resulting in an interactive Streamlit app.

The LangChain code, once generated, is not a mere endpoint but a transformative stage. It evolves into a user-friendly Streamlit application, adding an interactive dimension to the logic crafted. This metamorphosis embodies DemoGPT's commitment to user engagement and experience.

### Future Enhancements

We are planning to add a publicly available database that will accelerate the generation process by retrieving similar examples during the refining process. This innovation will further streamline the development workflow, making it more efficient and responsive.

### Model Flexibility

DemoGPT is designed to be adaptable, capable of using any LLM model that meets specific performance criteria in terms of code generation. This flexibility ensures that DemoGPT remains at the forefront of technology, embracing new advancements in LLM.

DemoGPT's iterative development process remains a cornerstone of its innovation. Each code segment undergoes individual testing, and the self-refining strategy ensures an efficient and error-minimized workflow. This fusion of meticulous testing and refinement is a testament to DemoGPT's pursuit of excellence.

By transcending traditional coding paradigms, DemoGPT is pioneering a new era in LLM-based applications. It's not just about code generation; it's about crafting intelligent, interactive, and inclusive solutions.

In summary, DemoGPT is more than a project; it's a visionary approach, pushing the boundaries of what's possible in LLM-based application development.

In the next release, we are gonna integrate **Gorilla** to DemoGPT to enable DemoGPT to use external APIs autonomously. The future is bright, and the journey has just begun. Join us in this exciting adventure!


## ⚙️ Architecture
### DemoGPT Architecture
![DemoGPT Architecture](assets/plan_based_pipeline.png?raw=true "DemoGPT Architecture")

## 🔧 Installation

### For the Package Version

You can install the DemoGPT package by running the following command:

```sh
pip install demogpt
```

### For the Source Code Version


1. Clone the repository:
    ```sh
    git clone https://github.com/melih-unsal/DemoGPT.git
    ```
2. Navigate into the project directory:
    ```sh
    cd DemoGPT
    ```
3. Install DemoGPT: 
    ```sh
    pip install .
    ```

## 🎮 Usage

### 📦 For the Package Version

Once the DemoGPT package is installed, you can use it by running the following command in your terminal:

```sh
demogpt
```

### 🐍 For the Python Interface

You can now use DemoGPT as a library in your Python applications:

```python
from demogpt import DemoGPT
agent = DemoGPT(model_name="gpt-3.5-turbo") # if OPENAI_API_KEY is not set in env variables, put it with openai_api_key argument
instruction = "Your instruction here"
title = "Your title here"
code = ""
for phase in agent(instruction=instruction, title=title):
    print(phase) # this will display the resulting json for each generation stage
    if phase["done"]:
        code = phase["code"] # final code
print(code)
```

Example Output (truncated):

```bash
# phases
{'stage': 'draft', 'completed': False, 'percentage': 60, ...}
{'stage': 'draft', 'completed': False, 'percentage': 64, 'code': '#Get the source language ...'}
...
{'stage': 'final', 'completed': True, 'percentage': 100, ... , 'code': 'import streamlit as st\n...'}
```

```python
# Code
import streamlit as st
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
...
```

### 🌐 For the Source Code Version

If you have cloned the repository and wish to run the source code version, you can use DemoGPT by running the following command:

```sh
streamlit run demogpt/app.py
```

## To-Do 📝
- [x] Implement new DemoGPT pipeline including plan generation, task creation, code snippet generation, and final code assembly.
- [x] Add feature to allow users to select models.
- [x] Define useful LangChain tasks
- [x] Publish release with the new pipeline without refinement
- [ ] Implement remaining LangChain tasks
- [ ] Implement self-refining strategy for model response refinement.
- [ ] Integrate 🦍 Gorilla model for API calls.
- [ ] Add Rapid API for expanding available API calls. 
- [ ] Add 🦙 Llama2 integration
- [ ] Implement publicly available database to accelerate the generation process by retrieving similar examples during the refining process.
- [ ] Add all successfully generated steps to a DB to eliminate redundant refinement.

## 🤝 Contribute

Contributions to the DemoGPT project are welcomed! Whether you're fixing bugs, improving the documentation, or proposing new features, your efforts are highly appreciated. Please check the open issues before starting any work.

> Please read [`CONTRIBUTING`](CONTRIBUTING.md) for details on our [`CODE OF CONDUCT`](CODE_OF_CONDUCT.md), and the process for submitting pull requests to us.

## 📄 Citations

DemoGPT has been referenced in various research papers for its innovative approach to app creation using autonomous AI agents. Below is a list of papers that have cited DemoGPT:

- Lei Wang, Chen Ma , Xueyang Feng , Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, Wayne Xin , Zhao, Zhewei Wei, Ji-Rong Wen, "A Survey on Large Language Model based Autonomous Agents", 2023. [Link to paper](https://arxiv.org/pdf/2308.11432.pdf)
- Yuan Li, Yixuan Zhang, Lichao Sun, "METAAGENTS: SIMULATING INTERACTIONS OF HUMAN BEHAVIORS FOR LLM-BASED TASK-ORIENTED COORDINATION VIA COLLABORATIVE GENERATIVE AGENTS" Journal/Conference, 2023. [Link to paper](https://arxiv.org/pdf/2310.06500.pdf)
- Yuheng Cheng, Ceyao Zhang, Zhengwen Zhang, Xiangrui Meng, Sirui Hong, Wenhao Li, Zihao Wang, Zekai Wang, Feng Yin, Junhua Zhao, Xiuqiang He, "EXPLORING LARGE LANGUAGE MODEL BASED INTELLIGENT AGENTS: DEFINITIONS, METHODS, AND PROSPECTS", 2024. [Link to paper](https://arxiv.org/pdf/2401.03428.pdf)
- Mikhail, Poludin. Optimalizace LLM agentů pro analýzu tabulkových dat: Integrace LoRA pro zvýšení kvality. MS thesis. České vysoké učení technické v Praze. Vypočetní a informační centrum., 2024. [Link to paper](https://dspace.cvut.cz/bitstream/handle/10467/115388/F3-DP-2024-Poludin-Mikhail-Optimizing_LLM-Powered_Agents_for_Tabular_Data_Analytics_Integrating_LoRA_for_Enhanced_Quality.pdf?sequence=-1)

This acknowledgment from the academic community highlights the potential and utility of DemoGPT in advancing the field of AI-driven development tools.


## 📜 License

DemoGPT is an open-source project licensed under [MIT License](LICENSE).

---

For any issues, questions, or comments, please feel free to contact us or open an issue. We appreciate your feedback to make DemoGPT better.
