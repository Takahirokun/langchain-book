import os
import chainlit as cl
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_redis import RedisChatMessageHistory  #← RedisChatMessageHistoryをインポート

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

chat = ChatOpenAI(
    model="gpt-3.5-turbo"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたは会話の文脈を考慮したチャットボットです。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)


def get_redis_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL)


@cl.on_chat_start
async def on_chat_start():
    thread_id = None
    while not thread_id: #← スレッドIDが入力されるまで繰り返す
        res = await cl.AskUserMessage(content="私は会話の文脈を考慮した返答ができるチャットボットです。スレッドIDを入力してください。", timeout=600).send() #← AskUserMessageを使ってスレッドIDを入力
        if res:
            thread_id = res['output']
            await cl.Message(
                content=f"スレッドIDを受け取りました: {thread_id}",
            ).send()

    print(f"Received thread_id: {thread_id}")
    history = RedisChatMessageHistory(  #← RedisChatMessageHistoryを初期化
        session_id=thread_id,
        redis_url=REDIS_URL,  
    )

    chain = prompt | chat

    chain_with_history = RunnableWithMessageHistory(
        chain, get_redis_history, input_messages_key="input", history_messages_key="history"
    )

    messages = history.messages

    for message in messages:
        print(f"Processing message: {message}")
        if isinstance(message, HumanMessage): #← ユーザーからのメッセージかどうかを判定
            await cl.Message( #← ユーザーからのメッセージの場合はauthorUserを指定して送信
                author="User",
                content=f"{message.content}",
            ).send()
        else:
            await cl.Message( #← AIからのメッセージの場合はChatBotを指定して送信
                author="ChatBot",
                content=f"{message.content}",
            ).send()
    cl.user_session.set("session_id", thread_id) #← セッションIDをセッションに保存
    cl.user_session.set("chain_with_history", chain_with_history) #← 履歴をセッションに保存

@cl.on_message
async def on_message(message: cl.Message):
    session_id = cl.user_session.get("session_id") 
    chain_with_history = cl.user_session.get("chain_with_history") 

    message_content = message.content

    result = chain_with_history.invoke(
        {"input": message_content},
        config={"configurable": {"session_id": session_id}},
    )

    await cl.Message(content=result.content).send() 
