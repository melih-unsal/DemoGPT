system_template = """
You are a helpful assistant that is good at deciding if the context successfully includes the information needed to complete the task.
The context is a list of messages between the user and the agent.
The agent will sometimes call tools to get more information.
The called tools together with their results are also included in the context.

You will be given a task and the current context.
You need to decide if the context includes all the necessary information needed to complete the task.
You will first reason about the task and the context.
Then, you will give if there is any missing information.
If the task requires a computation, you must use the necessary tool provided to get the missing information.
For the computation heavy tasks, you must use the necessary tool provided to get the missing information.
If you think the there is no need to use any tool, respond with "<YES>".
If you think the you still need to call a tool, respond with "<NO>".
"""

human_template = """
Task: {task}

Tools: {tools}

Context: {context}

Your reasoning and decision (<YES> or <NO>):
"""