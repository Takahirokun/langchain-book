import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

workflow = StateGraph(state_schema=MessagesState)

chat = ChatOpenAI(
    model="gpt-3.5-turbo"
)


def call_model(state: MessagesState):
    system_prompt = ("あなたは会話の文脈を考慮した返答をするチャットボットです。")
    system_message = SystemMessage(content=system_prompt)
    messages_history = state["messages"][:-1]  # 直近のユーザーのメッセージを除外

    print(f"現在のメッセージ数: {len(messages_history)}")
    # 会話履歴が規定の長さを超える場合は、メッセージを要約
    if len(messages_history) >= 4:
        last_human_message = state["messages"][-1]
        # 今までの会話を要約
        summary_prompt = (
            "上の会話を要約してください。"
            "要約は、会話の重要なポイントを含むようにしてください。"
        )
        summary_message = chat.invoke(
            messages_history + [HumanMessage(content=summary_prompt)]
        )
        print(f"要約メッセージ: {summary_message.content}")

        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"]] # 再度メッセージを追加
        human_message = HumanMessage(content=last_human_message.content)
        response = chat.invoke(
            [system_message, summary_message, human_message]
        )
        message_updates = [summary_message, human_message, response] + delete_messages
    else:
        message_updates = chat.invoke([system_message] + state["messages"])

    return {"messages": message_updates}


workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="私は会話の文脈を考慮した返答をできるチャットボットです。メッセージを入力してください。").send()

@cl.on_message
async def on_message(message: cl.Message):
    message_content = message.content

    result = app.invoke(
        {
            "messages": [HumanMessage(content=message_content)]
        },
        config={"configurable": {"thread_id": "2"}},
    )

    await cl.Message(content=result["messages"][-1].content).send()
