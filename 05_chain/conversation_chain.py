from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chat = ChatOpenAI()

chain = RunnableWithMessageHistory(chat, get_session_history)
chain.invoke(
    "iPhone11の発売日を教えて",
    config={"configurable": {"session_id": "1"}},
)

