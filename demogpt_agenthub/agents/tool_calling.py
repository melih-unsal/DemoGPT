from demogpt_agenthub.agents import BaseAgent

class ToolCallingAgent(BaseAgent):
    def __init__(self, tools, llm, verbose=False):
        super().__init__(tools, llm, verbose)
    
    def run(self, prompt):
        self.add_message("User", prompt)
        # Format tool explanations for better readability
        formatted_tools = "\nAvailable Tools:\n"
        for tool_name, details in self.tool_explanations.items():
            formatted_tools += f"\n{tool_name}:\n"
            formatted_tools += f"  Description: {details['description']}\n"
            formatted_tools += f"  {details['parameters']}\n"
            formatted_tools += f"  Run Function: {details['run_description']}\n"
        decision = self.tool_decider.invoke({"task": prompt, "context": self.context, "tools": formatted_tools})
        self.add_message("Agent", decision["reasoning"])
        self.pretty_print("Reasoning", decision["reasoning"])
        self.pretty_print("Tool call", decision["tool"])
        tool_call = self.tools[decision["tool"]]
        tool_args = decision["argument"]
        tool_result = tool_call.run(**tool_args)
        self.add_message(decision["tool"], tool_result)
        self.pretty_print("Tool result", tool_result)
        answer = self.final_answer.invoke({"query": prompt, "context": self.context})
        self.add_message("Agent", answer)
        self.pretty_print("Answer", answer)
        return answer

if __name__ == "__main__":
    from demogpt_agenthub.tools import DuckDuckGoSearchTool, WeatherTool, WikipediaTool    
    from demogpt_agenthub.llms import OpenAIChatModel
    search_tool = DuckDuckGoSearchTool()
    weather_tool = WeatherTool()
    wikipedia_tool = WikipediaTool()
    agent = ToolCallingAgent(tools=[search_tool, weather_tool, wikipedia_tool], llm=OpenAIChatModel(model_name="gpt-4o-mini"), verbose=True)
    query = "Who is Daron Acemoglu?"
    print(agent.run(query))