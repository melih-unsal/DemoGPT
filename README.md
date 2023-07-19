# ![favicon](assets/puzzle.png) DemoGPT: Auto Gen-AI App Generator with the Power of Llama 2

<p align="center">
<a href=""><img src="assets/banner_small.png" alt="DemoGPT logo: Generate automatic LangChain pipelines" width="450px"></a>
</p>

<p align="center">
<b>⚡ With just a prompt, you can create interactive Streamlit apps via 🦜️🔗 LangChain's transformative capabilities & Llama 2.⚡</b>
</p>

<p align="center">
<a href="https://github.com/melih-unsal/DemoGPT/releases"><img src="https://img.shields.io/github/release/melih-unsal/DemoGPT" alt="Releases"></a>
<a href="https://demogpt.io"><img src="https://img.shields.io/badge/Official%20Website-demogpt.io-blue?style=flat&logo=world&logoColor=white" alt="Official Website"></a>
<a href="https://melih-unsal.github.io/DemoGPT-Docs/"><img src="https://img.shields.io/badge/Documentation-📘-blueviolet" alt="DemoGPT Documentation"></a>
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
<a href="docs/resources/WeChat.jpeg"><img src="https://img.shields.io/badge/WeChat-微信-blue" alt="WeChat"></a>
<a href="https://twitter.com/demo_gpt"><img src="https://img.shields.io/twitter/follow/demo_gpt?style=social" alt="Twitter Follow"></a>
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

![Humor Machine](assets/humor_machine.gif)

https://github.com/melih-unsal/DemoGPT/assets/34304254/8991e296-b6fe-4817-bd08-4dab6d13020d

## 📚 Documentation

See our documentation site [here](https://melih-unsal.github.io/DemoGPT-Docs/) for full how-to docs and guidelines

⚡ The new release with the power of **Llama 2** is within a week. ⚡


## 📑 Table of Contents

- [Introduction](#-introduction)
- [Pipeline](#%EF%B8%8F-pipeline)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contribute](#-contribute)
- [License](#-license)

## 📌 Introduction

Welcome to DemoGPT, a ground-breaking open-source initiative aimed at optimizing and democratizing the development of Large Language Model (LLM) based applications. 

At the heart of DemoGPT lies the potent GPT-3.5-turbo, which enables the auto-generation of LangChain code. This process is fueled by a unique self-refining strategy that seamlessly blends document understanding from the LangChain documentation tree with user prompts. The outcome is a piece of code that doesn't just work, but is inherently robust, adhering to best coding practices while maintaining a deep-rooted alignment with the LangChain library.

The LangChain code, once generated, is not a final product but an intermediate stage. The code is further transformed into a user-friendly Streamlit application, adding an interactive layer to the logic produced.

Alongside this, DemoGPT embraces an iterative development process, wherein each code segment is individually tested. This approach, coupled with the self-refining strategy, enables an efficient and error-minimized workflow, pushing the envelope in traditional code development.

By making software development accessible through simple prompts, DemoGPT is laying the groundwork for a paradigm shift in how we create, refine, and customize LLM-based applications. The end goal is a broader, more inclusive ecosystem where users, regardless of their coding proficiency, can contribute to the continuous evolution of products. 

In summary, DemoGPT isn't just a project; it is a forward-thinking approach, redefining the boundaries of LLM-based application development.

In the next release, we are gonna add **Llama 2** inside of DemoGPT to make the whole system runnable completely locally.

## ⚙️ Architecture
### DemoGPT Architecture
![DemoGPT Architecture](assets/demogpt_new_pipeline1.jpeg?raw=true "DemoGPT Architecture")

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
