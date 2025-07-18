from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch

chat = ChatOpenAI(
    temperature=0,  #← temperatureを0に設定して出力の多様性を抑える
    model="gpt-3.5-turbo"
)

tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general"
)  #← TavilySearchを使用して最大5件の検索結果を取得するToolを作成

agent = create_react_agent(chat, [tavily_search_tool])  #← React Agentを作成

result = agent.invoke({"messages": [("human", "今日の東京の天気を調べてください。")]})

print(f"実行結果: {result["messages"][-1].content}")
