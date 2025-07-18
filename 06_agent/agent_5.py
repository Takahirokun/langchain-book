from langchain_core.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import WikipediaRetriever
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

memory = MemorySaver()

chat = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

retriever = WikipediaRetriever(
    lang="ja",
    doc_content_chars_max=500,
    top_k_results=1
)

tools= [
    create_retriever_tool(  #←Retrieversを使用するToolを作成
        name="WikipediaRetriever",  #←Toolの名前
        description="受け取った単語に関するWikipediaの記事を取得できる",  #←Toolの説明
        retriever=retriever,  #←Retrieversを指定
    ),
]

agent = create_react_agent(
    chat, tools, checkpointer=memory
)
config = {"configurable": {"thread_id": "test_thread"}}

result = agent.invoke(
    {
        "messages": [
            ("user", "スコッチウイスキーについてWikipediaで調べて日本語で概要をまとめてください。")
        ]
    },
    config,
)
print(f"1回目の実行結果: {result["messages"][-1].content}")

result2 = agent.invoke(
    {
        "messages": [
            ("user", "英語に翻訳してください。")
        ]
    },
    config,
)
print(f"2回目の実行結果: {result2["messages"][-1].content}") 
