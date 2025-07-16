import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.messages import trim_messages, HumanMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

messages = [
    SystemMessage(content="あなたは優秀なAIアシスタントです。"),
]

chat = ChatOpenAI(
    model="gpt-3.5-turbo"
)

chat_history = InMemoryChatMessageHistory(messages=messages[:-1])


def dummy_get_session_history(session_id: str):
    if session_id != "1":
        return InMemoryChatMessageHistory()
    return chat_history

trimmer = trim_messages(
    strategy="last",
    token_counter=len,
    max_tokens=3,
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    # start_on="human" makes sure we produce a valid chat history
    start_on="human",                                   
)

chain = trimmer | chat

chain_with_history = RunnableWithMessageHistory(chain, dummy_get_session_history)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="私は会話の文脈を考慮した返答ができるチャットボットです。メッセージを入力してください。").send()

@cl.on_message
async def on_message(message: cl.Message):
    message_content = message.content
    messages = chat_history.messages

    print(f"保存されているメッセージの数: {len(messages)}" # 保存されているメッセージの数を表示する
          )

    for saved_message in messages: # 保存されているメッセージを1つずつ取り出す
        print(saved_message.content)

    result = chain_with_history.invoke(
        [HumanMessage(content=message_content)],
        config={"configurable": {"session_id": "1"}},
    )

    await cl.Message(content=result.content).send()
