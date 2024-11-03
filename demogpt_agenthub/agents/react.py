from demogpt_agenthub.agents import BaseAgent

class ReactAgent(BaseAgent):
    def __init__(self, tools, llm, verbose=False):
        super().__init__(tools, llm, verbose)
    
    def ask(self, prompt):
        self.add_message("User", prompt)
        result_ready = False
        while not result_ready:
            decision = self.tool_decider.invoke({"task": prompt, "context": self.context, "tools": self.tool_explanations})
            self.add_message("Agent", decision["reasoning"])
            self.pretty_print("Reasoning", decision["reasoning"])
            self.pretty_print("Tool call", decision["tool"])
            tool_call = self.tools[decision["tool"]]
            tool_args = decision["args"]
            self.pretty_print("Tool args", tool_args)
            tool_result = tool_call.run(tool_args)
            self.add_message(decision["tool"], tool_result)
            self.pretty_print("Tool result", tool_result)
            result_ready = self.success_decider.invoke({"task": prompt, "context": self.context})
            self.pretty_print("Decision", result_ready)

        answer = self.final_answer.invoke({"query": prompt, "context": self.context})
        self.add_message("Agent", answer)
        self.pretty_print("Answer", answer)
        return answer

if __name__ == "__main__":
    from demogpt_agenthub.tools import DuckDuckGoSearchTool, WeatherTool, WikipediaTool    
    from demogpt_agenthub.llms import OpenAIChatModel
    search_tool = DuckDuckGoSearchTool()
    weather_tool = WeatherTool()
    agent = ReactAgent(tools=[search_tool, weather_tool], llm=OpenAIChatModel(model_name="gpt-4o-mini"), verbose=True)
    query = "What is the weather in the country where Christiano Ronaldo is currently playing?"
    print(agent.ask(query))