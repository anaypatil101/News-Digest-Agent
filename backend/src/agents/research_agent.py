from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.search import get_search_tool
from tools.fetcher import fetch_article
from tools.filter import filter_relevant_articles
from datetime import datetime


def create_research_agent():
    current_date = datetime.now().strftime("%B %Y") 
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

    search_tool = get_search_tool()
    tools = [search_tool, fetch_article, filter_relevant_articles]

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a news research agent. Today's date is {current_date}.

For each interest topic:
1. Search ONCE using a specific, targeted query — include the current month and year to get fresh results
   Good query example: "AI breakthroughs February 2026"
   Bad query example: "latest artificial intelligence news"
2. From the results keep the 2-3 most relevant and specific articles
3. Only fetch full content if the snippet is too vague

Return a structured list with:
- Title
- URL
- Brief snippet (2-3 sentences)
- Topic it belongs to

Be efficient — one search per topic is enough. Do not repeat searches."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=8
    )