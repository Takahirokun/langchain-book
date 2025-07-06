import json
from openai import OpenAI

client = OpenAI()  #←OpenAIが用意しているPythonパッケージをインポートする

response = client.chat.completions.create(#←OpenAIのAPIを呼び出すことで、言語モデルを呼び出している
    model="gpt-3.5-turbo",  #←呼び出す言語モデルの名前
    messages=[
        {
            "role": "user",
            "content": "iPhone8のリリース日を教えて"  #←入力する文章(プロンプト)
        },
    ])

print(response)
