from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.llms import OpenAIChatModel
from demogpt_agenthub.tools import DuckDuckGoSearchTool, WeatherTool, WikipediaTool

if __name__ == "__main__":
    search_tool = DuckDuckGoSearchTool()
    weather_tool = WeatherTool()
    agent = ToolCallingAgent(tools=[search_tool, weather_tool], llm=OpenAIChatModel(model_name="gpt-4o-mini"), verbose=True)
    query = "Who has won the Nobel Prize in Economics in 2024?"
    agent.ask(query)

