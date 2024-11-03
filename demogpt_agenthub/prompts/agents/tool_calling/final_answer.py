system_template = """
You are a helpful assistant that can answer the user query based on the provided context.
The context is a list of messages between the user and the assistant.
The assistant tried to find the answer using various tools.
Your job is to answer the user query based on the context.
Asnwer as a kind assistant.
"""

human_template = """
User: {query}
=============
Context:
{context}
=============
Answer:
"""
