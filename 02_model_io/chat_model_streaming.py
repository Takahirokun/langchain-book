from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

chat = ChatOpenAI(
    streaming=True,  #← streamingをTrueに設定し、ストリーミングモードで実行
    callbacks=[
        StreamingStdOutCallbackHandler()  #← StreamingStdOutCallbackHandlerをコールバックとして設定
    ]
)
resp = chat.invoke([ #← リクエストを送信
    HumanMessage(content="おいしいステーキの焼き方を教えて")
])
