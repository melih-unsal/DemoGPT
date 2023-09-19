# ![favicon](assets/puzzle.png) DemoGPT: Auto Gen-AI App Generator with the Power of Foundation Models

<p align="center">
<a href=""><img src="assets/banner_small.png" alt="DemoGPT logo: Generate automatic LangChain pipelines" width="450px"></a>
</p>

<p align="center">
<b>⚡ With just a prompt, you can create interactive Streamlit apps via 🦜️🔗 LangChain's transformative capabilities.⚡</b>
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

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=melih-unsal/DemoGPT&type=Timeline)](https://star-history.com/#melih-unsal/DemoGPT&Timeline)

⭐ Consider starring us if you're using DemoGPT so more people hear about us!

## 🔥 Demo

For quick demo, you can visit [our website](https://demogpt.io)

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


## 📑 Table of Contents

- [Introduction](#-introduction)
- [Architecture](#%EF%B8%8F-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [To-Do](#to-do-)
- [Contribute](#-contribute)
- [License](#-license)

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
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
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

## 📜 License

DemoGPT is an open-source project licensed under [MIT License](LICENSE).

---

For any issues, questions, or comments, please feel free to contact us or open an issue. We appreciate your feedback to make DemoGPT better.
