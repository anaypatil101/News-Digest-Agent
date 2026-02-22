import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

@tool
def fetch_article(url: str) -> str:
    """
    Fetch and extract the main text content from a news article URL.
    Input should be a valid URL string.
    Returns the cleaned article text.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract main text
        text = soup.get_text(separator="\n", strip=True)

        # Trim to avoid token overflow
        return text[:3000]
    
    except Exception as e:
        return f"Failed to fetch article: {str(e)}"