from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from langchain_community.agent_toolkits import FileManagementToolkit  #←ファイル書き込みできるToolをインポート

chat = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

tavily_search_tool = TavilySearch(max_results=5,topic="general")

tools = FileManagementToolkit(
    root_dir=str('./work'),
    selected_tools=["write_file", "read_file", "list_directory"],
).get_tools()

tools.append(tavily_search_tool)  # TavilySearchツールを追加

agent = create_react_agent(chat,tools)

result = agent.invoke({"messages": ["human","北海道の名産品を調べて日本語でresult.txtというファイルに保存してください。"]}) #←実行結果をファイルに保存するように指示

print(f"実行結果: {result["messages"][-1].content}")
