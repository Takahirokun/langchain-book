import chainlit as cl
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

chat = ChatOpenAI(
    temperature=0,  
    model="gpt-3.5-turbo"
)

tools = []

agent = create_react_agent(chat,tools=tools)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Agentの初期化が完了しました").send() 

@cl.on_message
async def on_message(input_message: cl.Message):
    result = agent.invoke( #← Agentを実行する
        {
            "messages": 
            [
                ("user", input_message.content)
            ]
        },
        config={"callbacks": [cl.LangchainCallbackHandler()]},
    )
    await cl.Message(content=result["messages"][-1].content).send()
