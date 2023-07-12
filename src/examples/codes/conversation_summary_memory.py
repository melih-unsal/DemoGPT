# Import necessary modules
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain.llms import OpenAI

# Create an instance of ConversationSummaryMemory
memory = ConversationSummaryMemory(llm=OpenAI(temperature=0))

# Save context in memory
memory.save_context({"input": "hi"}, {"output": "whats up"})

# Load memory variables
memory.load_memory_variables({})

# Print the conversation history
print(memory.buffer)

# Create another instance of ConversationSummaryMemory with return_messages=True
memory = ConversationSummaryMemory(llm=OpenAI(temperature=0), return_messages=True)

# Save context in memory
memory.save_context({"input": "hi"}, {"output": "whats up"})

# Load memory variables
memory.load_memory_variables({})

# Print the conversation history as a list of messages
print(memory.buffer)

# Get the messages from the memory
messages = memory.chat_memory.messages

# Set the previous summary
previous_summary = ""

# Predict the new summary
new_summary = memory.predict_new_summary(messages, previous_summary)

# Print the new summary
print(new_summary)

# Create a ChatMessageHistory object
history = ChatMessageHistory()

# Add user and AI messages to the history
history.add_user_message("hi")
history.add_ai_message("hi there!")

# Create an instance of ConversationSummaryMemory using the ChatMessageHistory
memory = ConversationSummaryMemory.from_messages(llm=OpenAI(temperature=0), chat_memory=history, return_messages=True)

# Print the conversation history
print(memory.buffer)

# Import necessary modules
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

# Create an instance of OpenAI language model
llm = OpenAI(temperature=0)

# Create a ConversationChain with ConversationSummaryMemory
conversation_with_summary = ConversationChain(
    llm=llm, 
    memory=ConversationSummaryMemory(llm=OpenAI()),
    verbose=True
)

# Predict the response for the input
response = conversation_with_summary.predict(input="Hi, what's up?")

# Print the response
print(response)

# Predict the response for the input
response = conversation_with_summary.predict(input="Tell me more about it!")

# Print the response
print(response)

# Predict the response for the input
response = conversation_with_summary.predict(input="Very cool -- what is the scope of the project?")

# Print the response
print(response)