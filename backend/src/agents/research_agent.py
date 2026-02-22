from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.search import get_search_tool
from tools.fetcher import fetch_article
from tools.filter import filter_relevant_articles

def create_research_agent():
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

    search_tool = get_search_tool()
    tools = [search_tool, fetch_article, filter_relevant_articles]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a news research agent. Your job is to find the latest and most relevant news articles based on the user's interests.

For each interest topic provided:
1. Search for the latest news on that topic
2. Fetch the full content of the most promising articles
3. Filter and keep only the most relevant ones

Return a structured list of relevant articles with:
- Title
- URL  
- Brief content snippet (2-3 sentences)
- Topic it belongs to

Be thorough but focused — quality over quantity."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=6
    )