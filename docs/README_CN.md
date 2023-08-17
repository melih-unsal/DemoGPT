# ![favicon](../assets/puzzle.png) DemoGPT：自动 LangChain 管道生成

<p align="center">
<a href=""><img src="../assets/banner_small.png" alt="DemoGPT logo：自动生成 LangChain 流程" width="350px"></a>
</p>

<p align="center">
<b>⚡ 仅使用提示即可快速创建演示。 ⚡</b>
</p>

<p align="center">
<a href="https://github.com/melih-unsal/DemoGPT/releases"><img src="https://img.shields.io/github/release/melih-unsal/DemoGPT" alt="版本"></a>
<a href="https://demogpt.io"><img src="https://img.shields.io/badge/官方网站-demogpt.io-blue?style=flat&logo=world&logoColor=white" alt="官方网站"></a>
<a href="https://melih-unsal.github.io/DemoGPT-Docs/)"><img src="https://img.shields.io/badge/文档-📘-blueviolet" alt="DemoGPT文档"></a>
</p>

<p align="center">
<a href="README_CN.md"><img src="https://img.shields.io/badge/文档-中文版-blue.svg" alt="CN doc"></a>
<a href="../README.md"><img src="https://img.shields.io/badge/document-English-blue.svg" alt="EN doc"></a>
<a href="ROADMAP_CN.md"><img src="https://img.shields.io/badge/ROADMAP-路线图-blue" alt="roadmap"></a>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

<p align="center">
<a href="https://github.com/melih-unsal/DemoGPT/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues/melih-unsal/DemoGPT.svg?maxAge=2592000000000000" alt="打开一个问题"></a>
<a href="https://github.com/melih-unsal/DemoGPT/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/melih-unsal/DemoGPT.svg?maxAge=25920000000000000000" alt="已关闭的问题"></a>
<a href="https://star-history.com/#melih-unsal/DemoGPT"><img src="https://img.shields.io/github/stars/melih-unsal/DemoGPT?style=social" alt="DemoGPT  星星"></a>
</p>

<p align="center">
<a href="https://twitter.com/demo_gpt"><img src="https://img.shields.io/twitter/follow/demo_gpt?style=social" alt="Twitter Follow"></a>
</p>

<p align="center">
<a href="https://demogpt.streamlit.app"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit应用"></a>
<a href="https://huggingface.co/spaces/melihunsal/demogpt"><img src="https://img.shields.io/badge/%F0%9F%A4%97-空间-yellow"></a>
</p>


## 🔥 演示

要快速演示，您可以访问[我们的网站](https://demogpt.io)

https://github.com/melih-unsal/DemoGPT/assets/34304254/8991e296-b6fe-4817-bd08-4dab6d13020d

## 📚 文档

请访问我们的[文档站点](https://melih-unsal.github.io/DemoGPT-Docs/)，查看完整的操作文档和指南

## 📑 目录

- [简介](#-简介)
- [管道](#%EF%B8%8F-管道)
- [安装](#-安装)
- [使用](#-使用)
- [贡献](#-贡献)
- [许可证](#-许可证)

## 📌 简介

DemoGPT 是一款创新的开源项目，旨在简化基于语言学习模型（LLM）的应用程序的开发。它利用 GPT-3.5-turbo 的能力，使用'Thought Tree' (ToT) 方法自动生成 LangChain 代码。传统上，LangChain 被用于为基于 LLM 的应用程序创建管道，而通过 DemoGPT，我们正在改变处理这些管道的方式。

这个过程是全自动的，DemoGPT 会生成代码，运行测试，并逐步开发项目。每一段代码都会被单独测试和评估。如果它通过了自动生成的测试，开发就会继续，从而实现高效和无误的开发。

## ⚙️ 架构
### DemoGPT 架构
![DemoGPT 架构](../assets/demogpt_new_pipeline1.jpeg?raw=true "DemoGPT Architecture")

## 🔧 安装

1. 克隆仓库：
    ```sh
    git clone https://github.com/melih-unsal/DemoGPT.git
    ```
2. 导航到项目目录：
    ```sh
    cd DemoGPT
    ```
3. 安装必要的依赖项： 
    ```sh
    pip install -r requirements.txt
    ```

## 🎮 使用

安装完成后，您可以通过运行以下命令使用 DemoGPT：

```sh
streamlit run src/prompt_based/app.py
```

## 🤝 贡献

欢迎为DemoGPT项目做出贡献！无论您是修复错误、改进文档还是提出新的功能，我们都非常感谢您的努力。在开始任何工作之前，请检查开放的问题。

> 请阅读[`CONTRIBUTING`](../CONTRIBUTING.md)以获取我们的[`CODE OF CONDUCT`](../CODE_OF_CONDUCT.md)的详细信息，以及向我们提交拉取请求的过程。

## 📜 许可证

DemoGPT是一个基于[MIT许可证](../LICENSE)的开源项目。

---

如有任何问题、疑问或评论，请随时与我们联系或提出问题。我们非常欣赏您的反馈，以使DemoGPT变得更好。