from demogpt.assistants import ToolCallingAssistant
from demogpt.llms import OpenAIChatModel
from demogpt.tools import DuckDuckGoSearchTool, WeatherTool, WikipediaTool

if __name__ == "__main__":
    search_tool = DuckDuckGoSearchTool()
    weather_tool = WeatherTool()
    assistant = ToolCallingAssistant(tools=[search_tool, weather_tool], llm=OpenAIChatModel(model_name="gpt-4o-mini"), verbose=True)
    query = "Who is Daron Acemoglu?"
    assistant.ask(query)

