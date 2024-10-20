from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

def get_prompt(system_template: str, human_template: str):
    prompts = []
    if system_template:
        prompts.append(SystemMessagePromptTemplate.from_template(system_template))
    if human_template:
        prompts.append(HumanMessagePromptTemplate.from_template(human_template))
    return ChatPromptTemplate.from_messages(prompts)
    
if __name__ == "__main__":
    system_template = "System: {system_message}"
    human_template = "Human: {human_message}"
    prompt = get_prompt(system_template, human_template)
    print(prompt)