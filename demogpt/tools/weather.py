import os
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_community.tools.openweathermap.tool import OpenWeatherMapQueryRun
from demogpt.tools import BaseTool

class WeatherTool(BaseTool):
    def __init__(self):
        api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
        if not api_key:
            raise ValueError('OPENWEATHERMAP_API_KEY environment variable is not set')
        wrapper = OpenWeatherMapAPIWrapper()
        self.tool = OpenWeatherMapQueryRun(api_wrapper=wrapper)
        super().__init__()
    
    def run(self, city):
        return self.tool.run(city)
    
if __name__ == '__main__':
    tool = WeatherTool()
    print(tool.run('London'))