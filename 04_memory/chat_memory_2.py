import chainlit as cl
from langchain_core.runnables.history import RunnableWithMessageHistory  #← RunnableWithMessageHistoryを追加
from langchain_core.chat_history import InMemoryChatMessageHistory  #← InMemoryChatMessageHistoryを追加
from langchain_openai import ChatOpenAI

store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chat = ChatOpenAI(
    model="gpt-3.5-turbo"
)

chain = RunnableWithMessageHistory(chat, get_session_history)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="私は会話の文脈を考慮した返答をできるチャットボットです。メッセージを入力してください。").send()

@cl.on_message
async def on_message(message: cl.Message):
    message_content = message.content

    result = chain.invoke( 
        message_content, #← ユーザーからのメッセージを引数に指定
        config={"configurable": {"session_id": "1"}},  #← セッションIDを指定
    )

    await cl.Message(content=result.content).send()
