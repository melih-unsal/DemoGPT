from demogpt_agenthub.tools import BaseTool
import requests

class BochaWebsearchTool(BaseTool):
    def __init__(self, BOCHA_API_KEY):
        self.name = "bocha_websearch_tool"
        self.description = "Perform web search using the Bocha Web Search API."
        self.BOCHA_API_KEY = BOCHA_API_KEY
        super().__init__()

    def run(self, query):
        url = 'https://api.bochaai.com/v1/web-search'  # Fixed trailing whitespace
        headers = {
            'Authorization': f'Bearer {self.BOCHA_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "query": query,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            json_response = response.json()
            print(json_response)
            try:
                if json_response["code"] != 200 or not json_response["data"]:
                    return f"Search API request failed, reason: {json_response.get('msg', 'unknown error')}"

                webpages = json_response["data"]["webPages"]["value"]
                return webpages
            except Exception as e:
                return f"Search API request failed, reason: failed to parse search results - {str(e)}"
        else:
            return f"Search API request failed, status code: {response.status_code}, error message: {response.text}"