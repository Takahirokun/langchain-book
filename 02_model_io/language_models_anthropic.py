from langchain_anthropic import ChatAnthropic  #← モジュールをインポート

model = ChatAnthropic(  #←クライアントを作成しchatへ保存
    model="claude-3-5-sonnet-20240620",  #← 呼び出すモデルを指定
)

result = model.invoke( #← 実行する
    [
    (
        "system", "あなたはAIアシスタントです。質問に対して日本語で、コンシェルジュのように丁寧に答えてください。"
    ),  #← システムメッセージ"
    ("human", "こんにちは、あなたは誰ですか？"),  #← ユーザーメッセージ
    ]
)
print(result.content)
