from langchain_core.tools.retriever import create_retriever_tool  #← create_retriever_toolをインポート
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import WikipediaRetriever #←WikipediaRetrieverをインポート
from langchain_community.agent_toolkits import FileManagementToolkit
from langgraph.prebuilt import create_react_agent

chat = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

tools = FileManagementToolkit(
    root_dir=str("./work"),
    selected_tools=["write_file", "read_file", "list_directory"],  #←ファイル管理ツールを選択
).get_tools()  #←ファイル管理ツールを取得

retriever = WikipediaRetriever( #←WikipediaRetrieverを初期化
    lang="ja", #←言語を日本語に設定
    doc_content_chars_max=500,  #←記事の最大文字数を500文字に設定
    top_k_results=1 #←検索結果の上位1件を取得
)

tools.append(
    create_retriever_tool(  #←Retrieversを使用するToolを作成
        name="WikipediaRetriever",  #←Toolの名前
        description="受け取った単語に関するWikipediaの記事を取得できる",  #←Toolの説明
        retriever=retriever,  #←Retrieversを指定
    )
)

agent = create_react_agent(chat,tools=tools)

query = "スコッチウイスキーについてWikipediaで調べて概要を日本語でresult.txtというファイルに保存してください。"
result = agent.invoke({"messages": ["human", query]})

print(f"実行結果: {result["messages"][-1].content}")
