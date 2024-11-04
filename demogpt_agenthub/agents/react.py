from demogpt_agenthub.agents import BaseAgent

class ReactAgent(BaseAgent):
    def __init__(self, tools, llm, verbose=False, max_iter=10):
        super().__init__(tools, llm, verbose, max_iter)
    
    def ask(self, prompt):
        self.add_message("User", prompt)
        result_ready = False
        iter = 0
        while not result_ready and iter < self.max_iter:
            result_ready = self.success_decider.invoke({"task": prompt, "context": self.context, "tools": self.tool_explanations})
            self.pretty_print("Decision", result_ready)
            if result_ready:
                break
            decision = self.tool_decider.invoke({"task": prompt, "context": self.context, "tools": self.tool_explanations})
            self.add_message("Agent", decision["reasoning"])
            self.pretty_print("Reasoning", decision["reasoning"])
            self.pretty_print("Tool call", decision["tool"])
            tool_call = self.tools[decision["tool"]]
            tool_args = decision["argument"]
            self.pretty_print("Tool args", tool_args)
            tool_result = tool_call.run(tool_args)
            self.add_message(decision["tool"], tool_result)
            self.pretty_print("Tool result", tool_result)
            iter += 1
        if not result_ready:
            self.pretty_print("Not Completed", """The task was not completed within the maximum number of iterations. The agent will try to answer with the available context.
                              If you want to try again, you can increase the maximum number of iterations by setting the max_iter parameter when creating the agent.""")
        answer = self.final_answer.invoke({"query": prompt, "context": self.context})
        self.add_message("Agent", answer)
        self.pretty_print("Answer", answer)
        return answer

if __name__ == "__main__":
    from demogpt_agenthub.tools import DuckDuckGoSearchTool, WeatherTool, PythonTool
    from demogpt_agenthub.llms import OpenAIChatModel
    search_tool = DuckDuckGoSearchTool()
    weather_tool = WeatherTool()
    python_tool = PythonTool()
    agent = ReactAgent(tools=[search_tool, weather_tool, python_tool], llm=OpenAIChatModel(model_name="gpt-4o-mini"), verbose=True)
    query = "What is the weather's temperature's square root in the country where Christiano Ronaldo is currently playing? Please precisely calculate the result."
    print(agent.ask(query))