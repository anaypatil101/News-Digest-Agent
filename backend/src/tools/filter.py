from langchain_core.tools import tool

@tool
def filter_relevant_articles(input_str: str) -> str:
    """
    Filter and score articles based on relevance to user interests.
    Input should be a string in format: 'interests: AI, cricket | articles: title1, title2, title3'
    Returns a filtered list of the most relevant article titles.
    """
    try:
        parts = input_str.split("|")
        interests = parts[0].replace("interests:", "").strip()
        articles = parts[1].replace("articles:", "").strip()
        
        return f"Filtering articles for interests: {interests}\nArticles to evaluate: {articles}\nReturn only articles directly relevant to the interests."
    
    except Exception as e:
        return f"Filter error: {str(e)}"