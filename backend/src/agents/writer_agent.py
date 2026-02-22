from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_writer_agent():
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a news digest writer. Your job is to take raw research articles and transform them into a clean, engaging, personalized news digest.

Structure the digest as follows:

# 📰 Your Personalized News Digest

For each topic, create a section like:
## 🔍 [Topic Name]

For each article under that topic:
**[Article Title]**
[2-3 sentence summary of the article]
🔗 Source: [URL]

---

Guidelines:
- Write summaries in clear simple English
- Be concise but informative
- Maintain a neutral journalistic tone
- Group articles by topic
- End with a brief overall summary of today's digest"""),
        ("human", "{research}")
    ])

    chain = prompt | llm | StrOutputParser()
    return chain