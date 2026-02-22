from langchain_tavily import TavilySearch

def get_search_tool():
    return TavilySearch(
        max_results=5,
        topic="news",  # ← forces Tavily to search news sources specifically
        days=7,        # ← only return articles from the last 7 days
        description=(
            "Search for latest news articles on a given topic. "
            "Input should be a specific search query including the current month and year. "
            "Returns recent news articles with title, url and content snippet."
        )
    )
