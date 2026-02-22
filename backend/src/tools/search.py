from langchain_tavily import TavilySearch

def get_search_tool():
    return TavilySearch(
        max_results=5,
        description=(
            "Search the web for latest news articles on a given topic. "
            "Input should be a search query string. "
            "Returns a list of relevant articles with title, url and content snippet."
        )
    )