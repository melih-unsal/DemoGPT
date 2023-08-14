# DemoGPT Python Interface

DemoGPT now offers a Python interface, enabling seamless integration into your Python applications.

## 🐍 Using the Python Interface

To incorporate DemoGPT into your Python applications, follow the steps below.

### Integration Steps:

#### 1. Import the necessary module:
```python
from demogpt import DemoGPT
```

#### 2.Instantiate the DemoGPT agent:

To initialize the DemoGPT agent, use the `DemoGPT` class. It accepts three arguments:

   - **`model_name`**: Specifies the name of the model you wish to use. By default, this is set to `"gpt-3.5-turbo-0613"`.
   - **`openai_api_key`**: This is where you input your OpenAI API key. If you haven't set the `OPENAI_API_KEY` in your environment variables, you can pass it directly using this argument.
   - **`max_steps`**: This determines the number of steps used for refining the model's response during the internal workflow. By default, this is set 10

```python
agent = DemoGPT(model_name="gpt-3.5-turbo-0613", openai_api_key="YOUR_API_KEY", max_steps=10)
```

#### 3.Set your instruction and title:
```python
instruction = "Your instruction here"
title = "Your title here"
```

#### 4.Iterate through the generation stages and extract the final code:
```python
code = ""
for phase in agent(instruction=instruction, title=title):
    print(phase)  # This will display the resulting JSON for each generation stage.
    if phase["done"]:
        code = phase["code"]  # Extract the final code.
print(code)
```

### Generation Stages:

DemoGPT progresses through various stages to produce the final code. During each stage, it returns a JSON object containing the following key-value pairs:

- `stage`: The current stage, which could be "plan", "task", "draft", or "final".
- `completed`: A boolean indicating whether the stage has completed.
- `percentage`: Represents the progress percentage of the code generation.
- `done`: A boolean indicating if the entire process has been completed.
- `message`: An informational message about the current stage's status.

### Example Output:

Upon executing the steps mentioned above, you will receive outputs pertaining to each stage. Here's a condensed example of what you might see:

```bash
# phases
{'stage': 'draft', 'completed': False, 'percentage': 60, ...}
{'stage': 'draft', 'completed': False, 'percentage': 64, 'code': '#Get the source language ...'}
...
{'stage': 'final', 'completed': True, 'percentage': 100, ... , 'code': 'import streamlit as st\n...'}
```

```python
"""
Code response for the following arguments:
instruction = "Create a system that can translate from one language to another"
title = "My Translator"
"""

import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document

def translator(text, source_language, target_language):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0
    )
    system_template = """You are a language translator. Your task is to translate text from {source_language} to {target_language}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please translate the following text from {source_language} to {target_language}: '{text}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(text=text, source_language=source_language, target_language=target_language)
    return result  # returns string

st.title("My Translator")

# Initialize state variables
source_language = ""
target_language = ""
text = ""
translated_text = ""

# Get the source language from the user
source_language = st.text_input("Enter the source language")

# Get the target language from the user
target_language = st.text_input("Enter the target language")

# Get the text to be translated from the user
text = st.text_area("Enter the text to be translated")

# Create a button to trigger the translation
if st.button("Translate"):
    if text and source_language and target_language:
        translated_text = translator(text, source_language, target_language)
    else:
        translated_text = ""

# Display the translated text to the user
st.markdown(translated_text)
```
