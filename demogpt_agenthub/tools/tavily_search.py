from demogpt_agenthub.tools.base import BaseTool

class TavilySearchTool(BaseTool):
    def __init__(self, max_results=5, topic="general", search_depth="basic"):
        from langchain_tavily import TavilySearch
        self.tool = TavilySearch(
            max_results=max_results,
            topic=topic,
            search_depth=search_depth,
        )
        super().__init__()
        self.name = "TavilySearch"
        self.description = """A search engine tool that can find information on the internet.
        It is useful for answering questions about current events, facts, and general knowledge.
        It gets a search query as input and returns relevant search results."""

    def run(self, query: str):
        results = self.tool.invoke({"query": query})
        if isinstance(results, list):
            return "\n\n".join(
                r.get("content", str(r)) if isinstance(r, dict) else str(r)
                for r in results
            )
        return str(results)

if __name__ == "__main__":
    tool = TavilySearchTool()
    print(tool.run("What is the capital of France?"))
