from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from demogpt_agenthub.prompts import tool_decider, final_answer

from dotenv import load_dotenv

load_dotenv()

class BaseAssistant:
    def __init__(self, tools, llm, verbose=False):
        self.llm = llm
        self.tool_decider_prompt = ChatPromptTemplate.from_messages([
            ("system", tool_decider.system_template),
            ("human", tool_decider.human_template)
        ])
        self.tool_decider = self.tool_decider_prompt | self.llm | JsonOutputParser()
        self.final_answer_prompt = ChatPromptTemplate.from_messages([
            ("system", final_answer.system_template),
            ("human", final_answer.human_template)
        ])
        self.final_answer = self.final_answer_prompt | self.llm | StrOutputParser()
        self.history = []
        self.tools = tools
        self.verbose = verbose
        self.tools = {tool.name: tool for tool in tools}

    @property
    def tool_explanations(self):
        return {f"{tool.name}: {tool.description}" for tool in self.tools.values()}

    @property
    def context(self):
        return "\n".join([f"{name}: {message}" for name, message in self.history])
    
    def add_message(self, name, message):
        self.history.append((name, message))

    def pretty_print(self, message_type, content):
        """
        Displays the given content with color-coded formatting based on the message type.

        Args:
            message_type (str): The type of message (e.g., "Decision", "Tool call", "Tool result", "Answer").
            content (str): The content to be displayed.
        """
        color_codes = {
            "Decision": "\033[92m",  # Green
            "Tool call": "\033[94m",  # Blue
            "Tool result": "\033[93m",  # Yellow
            "Answer": "\033[95m"  # Magenta
        }

        if message_type in color_codes:
            print(f"{message_type}:")
            print(f"{color_codes[message_type]}{content}\033[0m")
        else:
            print(f"{message_type}:")
            print(content)
    
    def ask(self, prompt: str):
        """
        Abstract method to process a user's prompt and return a response.

        This method should be implemented by subclasses to define the specific
        behavior of how the assistant processes and responds to user prompts.

        Args:
            prompt (str): The user's input prompt or question.

        Returns:
            str: The assistant's response to the user's prompt.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the 'ask' method.")