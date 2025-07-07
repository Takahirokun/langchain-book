from langchain_openai import ChatOpenAI  #← モジュールをインポート
from langchain.schema import HumanMessage  #← ユーザーからのメッセージであるHumanMessageをインポート

model = ChatOpenAI(  #←クライアントを作成しchatへ保存
    model="gpt-3.5-turbo",  #← 呼び出すモデルを指定
)

result = model.invoke( #← 実行する
    [
        HumanMessage(content="iPhone8のリリース日を教えてください。"),
    ]
)
print(result.content)
