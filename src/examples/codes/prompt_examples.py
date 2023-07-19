# Chat models are a variation on language models. While chat models use language models under the hood, the interface they expose is a bit different: rather than expose a "text in, text out" API, they expose an interface where "chat messages" are the inputs and outputs.

# You can get chat completions by passing one or more messages to the chat model. The response will be a message. The types of messages currently supported in LangChain are AIMessage, HumanMessage, SystemMessage, and ChatMessage -- ChatMessage takes in an arbitrary role parameter. Most of the time, you'll just be dealing with HumanMessage, AIMessage, and SystemMessage.

# Most of the time, to use LangChain library, you need these imports below:

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Here are the examples:

# Goal: Generate blog post from title. Generate at least 500 words
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def generateBlogPost(title):
    chat = ChatOpenAI(
        temperature=0.1
    )  # Here temperature is set a little bit higher to put some variation

    template = "You are a helpful assistant that generates a blog post from the title: {title}. Please provide some content."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{title}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(title=title)
    return result  # it will return string with at least 500 words.


title = "Rise of AI"
blog = generateBlogPost(title)
print(blog)
######################################################################################################################################
# Goal: Implement language translation
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def generateTranslation(input_language, output_language, text):
    chat = ChatOpenAI(
        temperature=0
    )  # Here temperature is set to 0 because translation should be concrete

    template = "You are a helpful assistant that translates {input_language} to {output_language}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(
        input_language=input_language, output_language=output_language, text=text
    )
    return result  # it will return string


input_language = "English"
output_language = "French"
text = "How are you?"
transalated_text = generateTranslation(input_language, output_language, text)
print(transalated_text)
######################################################################################################################################
# Goal: Generate animal name from animal
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def generateAnimalName(animal):
    chat = ChatOpenAI(
        temperature=0.1
    )  # Here temperature is set a little bit higher to put some variation

    template = "You are a helpful assistant that generates a name for an animal. You generate short answer."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "What is a good name for a {animal}?"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(animal=animal)
    return result  # it will return string


animal = "dog"
animal_name = generateAnimalName(animal)
print(animal_name)
######################################################################################################################################
# Goal: Generate programming related humor
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def generateHumor():
    chat = ChatOpenAI(
        temperature=0.7
    )  # Here temperature is set a little bit higher to put some creativity

    template = (
        "You are a helpful assistant that generates a humor related to programming."
    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(
        {}
    )  # We don't need argument, what's why we needed to put an empty dictionary. Otherwise, it will give an error
    return result  # it will return string


humor = generateHumor()
print(humor)
######################################################################################################################################
# Goal: Generate random songs
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def generateSong():
    chat = ChatOpenAI(
        temperature=0.7
    )  # Here temperature is set a little bit higher to put some creativity

    template = "You are a helpful assistant that generate random song"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(
        {}
    )  # We don't need argument, what's why we needed to put an empty dictionary. Otherwise, it will give an error
    return result  # it will return string


song = generateSong()
print(song)
