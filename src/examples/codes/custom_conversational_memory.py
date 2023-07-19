# How to customize conversational memory

# Import necessary modules
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

# Create an instance of OpenAI
llm = OpenAI(temperature=0)

# Set the AI prefix in the conversation summary
# By default, it is set to "AI"
conversation = ConversationChain(
    llm=llm, verbose=True, memory=ConversationBufferMemory()
)

# Predict the response for the input "Hi there!"
conversation.predict(input="Hi there!")

# Predict the response for the input "What's the weather?"
conversation.predict(input="What's the weather?")

# Override the AI prefix and set it to "AI Assistant"
from langchain.prompts.prompt import PromptTemplate

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)

# Predict the response for the input "Hi there!"
conversation.predict(input="Hi there!")

# Predict the response for the input "What's the weather?"
conversation.predict(input="What's the weather?")

# Change the Human prefix in the conversation summary
# Set it to "Friend"
from langchain.prompts.prompt import PromptTemplate

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Friend: {input}
AI:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(human_prefix="Friend"),
)

# Predict the response for the input "Hi there!"
conversation.predict(input="Hi there!")

# Predict the response for the input "What's the weather?"
conversation.predict(input="What's the weather?")
