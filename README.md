# ![favicon](./puzzle.png) DemoGPT
⚡ Create quick demos by just using prompt. ⚡

[![Release Notes](https://img.shields.io/github/release/melih-unsal/DemoGPT)](https://github.com/melih-unsal/DemoGPT/releases)
[![Official Website](https://img.shields.io/badge/Official%20Website-demogpt.io-blue?style=flat&logo=world&logoColor=white)](https://demogpt.io)
[![GitHub star chart](https://img.shields.io/github/stars/melih-unsal/DemoGPT?style=social)](https://star-history.com/#melih-unsal/DemoGPT)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Twitter Follow](https://img.shields.io/twitter/follow/demo_gpt?style=social)](https://twitter.com/demo_gpt)
[![GitHub issues open](https://img.shields.io/github/issues/melih-unsal/DemoGPT.svg?maxAge=259200000)](https://github.com/melih-unsal/DemoGPT/issues?q=is%3Aopen+is%3Aissue) 
[![GitHub issues closed](https://img.shields.io/github/issues-closed-raw/melih-unsal/DemoGPT.svg?maxAge=259200000)](https://github.com/melih-unsal/DemoGPT/issues?q=is%3Aissue+is%3Aclosed)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://demogpt.streamlit.app)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Spaces-yellow)](https://huggingface.co/spaces/melihunsal/demogpt)

![DemoGPT](demogpt_new_banner.jpeg)

## 🔥 Demo

For quick demo, you can visit [our website](https://demogpt.io)

https://github.com/melih-unsal/DemoGPT/assets/34304254/8991e296-b6fe-4817-bd08-4dab6d13020d

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

## ⚙️ Pipeline
### DemoGPT Pipeline
![DemoGPT Pipeline](demogpt_pipeline.png?raw=true "DemoGPT Pipeline")

## 🔧 Installation

To get started with DemoGPT, you'll first need to clone the repository:
```
git clone https://github.com/melih-unsal/DemoGPT.git
```

Next, navigate to the project directory:
```
cd DemoGPT
```

Then, install the necessary dependencies. 
```
pip install -r requirements.txt
```

## 🎮 Usage

To use DemoGPT, you can run the command below:

```
streamlit run src/prompt_based/app.py
```

## 🤝 Contribute

Contributions to the DemoGPT project are welcomed! Whether you're fixing bugs, improving the documentation, or proposing new features, your efforts are highly appreciated. Please check the open issues before starting any work.

> Please read [`CONTRIBUTING`](CONTRIBUTING.md) for details on our [`CODE OF CONDUCT`](CODE_OF_CONDUCT.md), and the process for submitting pull requests to us.

## 📜 License

DemoGPT is an open-source project licensed under [MIT License](LICENSE).

---

For any issues, questions, or comments, please feel free to contact us or open an issue. We appreciate your feedback to make DemoGPT better.
