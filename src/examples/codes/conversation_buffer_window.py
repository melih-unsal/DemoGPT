# Conversation buffer window memory

# Import the required module
from langchain.memory import ConversationBufferWindowMemory

# Create an instance of ConversationBufferWindowMemory with k=1
memory = ConversationBufferWindowMemory(k=1)

# Save the context of the conversation
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context({"input": "not much you"}, {"output": "not much"})

# Load the memory variables
memory.load_memory_variables({})

# Print the history
print(memory.history)  # Output: 'Human: not much you\nAI: not much'

# Create another instance of ConversationBufferWindowMemory with k=1 and return_messages=True
memory = ConversationBufferWindowMemory(k=1, return_messages=True)

# Save the context of the conversation
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context({"input": "not much you"}, {"output": "not much"})

# Load the memory variables
memory.load_memory_variables({})

# Print the history as a list of messages
print(memory.history)  # Output: [HumanMessage(content='not much you', additional_kwargs={}), AIMessage(content='not much', additional_kwargs={})]

# Import the required modules
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

# Create an instance of ConversationChain with ConversationBufferWindowMemory
conversation_with_summary = ConversationChain(
    llm=OpenAI(temperature=0),
    memory=ConversationBufferWindowMemory(k=2),
    verbose=True
)

# Predict the response for the input "Hi, what's up?"
print(conversation_with_summary.predict(input="Hi, what's up?"))

# Predict the response for the input "What's their issues?"
print(conversation_with_summary.predict(input="What's their issues?"))

# Predict the response for the input "Is it going well?"
print(conversation_with_summary.predict(input="Is it going well?"))

# Predict the response for the input "What's the solution?"
print(conversation_with_summary.predict(input="What's the solution?"))