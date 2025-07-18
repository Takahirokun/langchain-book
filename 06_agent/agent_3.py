import random  #←ランダムな数字を生成するために必要なモジュールをインポート
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import FileManagementToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

chat = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

tools = FileManagementToolkit(
    root_dir=str("./work"),
    selected_tools=["write_file", "read_file", "list_directory"],
).get_tools()
 


@tool
def min_limit_random_number(min_number: int) -> int: #←最小値を指定できるランダムな数字を生成する関数
    """Generate a random number greater than or equal to the specified minimum number."""
    return random.randint(int(min_number), 100000)


tools.append(  #←ツールを追加
    min_limit_random_number
)

agent = create_react_agent(chat,tools=tools)

result = agent.invoke({"messages": ["human", "10以上のランダムな数字を生成してrandom.txtというファイルに保存してください。"]})

print(f"実行結果: {result["messages"][-1].content}")
