# ![favicon](./puzzle.png) DemoGPT: Auto LangChain Pipeline Generation

<p align="center">
<a href=""><img src="demogpt_new_banner.jpeg" alt="DemoGPT logo: Generate automatic LangChain pipelines" width="350px"></a>
</p>

<p align="center">
<b>⚡ Create quick demos by just using prompt. ⚡</b>
</p>

<p align="center">
<a href="https://github.com/melih-unsal/DemoGPT/releases"><img src="https://img.shields.io/github/release/melih-unsal/DemoGPT" alt="Releases"></a>
<a href="https://demogpt.io"><img src="https://img.shields.io/badge/Official%20Website-demogpt.io-blue?style=flat&logo=world&logoColor=white" alt="Official Website"></a>
<a href="https://melih-unsal.github.io/DemoGPT-Docs/)"><img src="https://img.shields.io/badge/Documentation-📘-blueviolet" alt="DemoGPT Documentation"></a>
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
</p>

<p align="center">
<a href="docs/resources/MetaGPT-WeChat-Personal.jpeg"><img src="https://img.shields.io/badge/WeChat-微信-blue" alt="WeChat"></a>
<a href="https://twitter.com/demo_gpt"><img src="https://img.shields.io/twitter/follow/demo_gpt?style=social" alt="Twitter Follow"></a>
</p>

<p align="center">
<a href="https://demogpt.streamlit.app"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit application"></a>
<a href="https://huggingface.co/spaces/melihunsal/demogpt"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Spaces-yellow"></a>
</p>

## 🔥 Demo

For quick demo, you can visit [our website](https://demogpt.io)

https://github.com/melih-unsal/DemoGPT/assets/34304254/8991e296-b6fe-4817-bd08-4dab6d13020d

## 📚 Documentation

See our documentation site [here](https://melih-unsal.github.io/DemoGPT-Docs/) for full how-to docs and guidelines


## 📑 Table of Contents

- [Introduction](#-introduction)
- [Pipeline](#%EF%B8%8F-pipeline)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contribute](#-contribute)
- [License](#-license)

## 📌 Introduction

DemoGPT is an innovative open-source project designed to streamline the development of Language Learning Model (LLM) based applications. It leverages the capabilities of GPT-3.5-turbo to auto-generate LangChain code using a 'Tree of Thoughts' (ToT) approach. LangChain is traditionally used for creating pipelines for LLM-based applications, and with DemoGPT, we are transforming the way we handle these pipelines. 

The process is fully automated, with DemoGPT generating code, running tests, and progressively developing the project step by step. Each piece of code is tested and evaluated by itself. If it passes the auto-generated tests, the development proceeds, allowing for efficient and error-free development.

## ⚙️ Architecture
### DemoGPT Architecture
![DemoGPT Architecture](demogpt_pipeline.png?raw=true "DemoGPT Architecture")

## 🔧 Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/melih-unsal/DemoGPT.git
    ```
2. Navigate into the project directory:
    ```sh
    cd DemoGPT
    ```
3. Install the necessary dependencies: 
    ```sh
    pip install -r requirements.txt
    ```

## 🎮 Usage

Once installed, you can use DemoGPT by running the following command:

```sh
streamlit run src/prompt_based/app.py
```

## 🤝 Contribute

Contributions to the DemoGPT project are welcomed! Whether you're fixing bugs, improving the documentation, or proposing new features, your efforts are highly appreciated. Please check the open issues before starting any work.

> Please read [`CONTRIBUTING`](CONTRIBUTING.md) for details on our [`CODE OF CONDUCT`](CODE_OF_CONDUCT.md), and the process for submitting pull requests to us.

## 📜 License

DemoGPT is an open-source project licensed under [MIT License](LICENSE).

---

For any issues, questions, or comments, please feel free to contact us or open an issue. We appreciate your feedback to make DemoGPT better.
