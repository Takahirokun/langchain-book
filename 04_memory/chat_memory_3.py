import os  #← 環境変数を取得するためにosをインポート
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

history = RedisChatMessageHistory(  #← RedisChatMessageHistoryを初期化
    session_id="chat_history",
    redis_url=REDIS_URL,  
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたは会話の文脈を考慮したチャットボットです。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

chain = prompt | chat


def get_redis_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL)

chain_with_history = RunnableWithMessageHistory(
    chain, get_redis_history, input_messages_key="input", history_messages_key="history"
)


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="私は会話の文脈を考慮した返答をできるチャットボットです。メッセージを入力してください。").send()


@cl.on_message
async def on_message(message: cl.Message):
    message_content = message.content

    result = chain_with_history.invoke(
        {"input": message_content},
        config={"configurable": {"session_id": "chat_history"}},
    )

    await cl.Message(content=result.content).send()
