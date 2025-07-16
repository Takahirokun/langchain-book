import chainlit as cl
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


def call_model(state: MessagesState):
   system_prompt = "あなたは親切で有能なアシスタントです。"
   messages = [SystemMessage(content=system_prompt)] + state["messages"]
   response = chat.invoke(messages)
   return {"messages": response} 

chat = ChatOpenAI(
    model="gpt-3.5-turbo"
)

workflow = StateGraph(state_schema=MessagesState)

workflow.add_node("model",call_model)
workflow.add_edge(START, "model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory) 


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="私は会話の文脈を考慮した返答ができるチャットボットです。メッセージを入力してください。").send()


@cl.on_message
async def on_message(message: cl.Message):
    result = app.invoke(
        {"messages": [HumanMessage(content=message.content)]},
        config={"configurable": {"thread_id": "1"}},
    )
    await cl.Message(content=result["messages"][-1].content).send() #← AIからのメッセージを送信
