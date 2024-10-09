import os
from langchain_community.utilities import OpenWeatherMapAPIWrapper

class WeatherTool:
    def __init__(self):
        api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
        if not api_key:
            raise ValueError('OPENWEATHERMAP_API_KEY environment variable is not set')
        self.tool = OpenWeatherMapAPIWrapper()
    
    def run(self, city):
        return self.tool.run(city)
    
if __name__ == '__main__':
    tool = WeatherTool()
    print(tool.run('London'))