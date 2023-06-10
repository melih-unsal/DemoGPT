# DemoGPT

![DemoGPT](DemoGPT_banner.png)


## Table of Contents

- [Introduction](#introduction)
- [Pipeline](#pipeline)
- [Installation](#installation)
- [Usage](#usage)
- [Contribute](#contribute)
- [License](#license)

## Introduction

DemoGPT is an innovative open-source project designed to streamline the development of Language Learning Model (LLM) based applications. It leverages the capabilities of GPT-3.5-turbo to auto-generate LangChain code using a 'Tree of Thoughts' (ToT) approach. LangChain is traditionally used for creating pipelines for LLM-based applications, and with DemoGPT, we are transforming the way we handle these pipelines. 

The process is fully automated, with DemoGPT generating code, running tests, and progressively developing the project step by step. Each piece of code is tested and evaluated by itself. If it passes the auto-generated tests, the development proceeds, allowing for efficient and error-free development.

## Pipeline
### DemoGPT Sequence Diagram
![DemoGPT Pipeline](pipeline.png?raw=true "DemoGPT Pipeline")

## Installation

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
You will then need to set the environment variable in the terminal.

```
export OPENAI_API_KEY="..."
```

Alternatively, you could do this from inside the Jupyter notebook (or Python script):
```
import os
os.environ["OPENAI_API_KEY"] = "..."
```

Note: Further instructions about dependencies will be added as the project develops.

## Usage

To use DemoGPT, you can follow these steps:

Note: The detailed steps on how to use the project will be added as the project develops.

## Contribute

Contributions to the DemoGPT project are welcomed! Whether you're fixing bugs, improving the documentation, or proposing new features, your efforts are highly appreciated. Please check the open issues before starting any work.

## License

DemoGPT is an open-source project licensed under [MIT License](LICENSE).

---

For any issues, questions, or comments, please feel free to contact us or open an issue. We appreciate your feedback to make DemoGPT better.