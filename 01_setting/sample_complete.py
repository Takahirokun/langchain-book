import json
from openai import OpenAI

client = OpenAI()

response = client.completions.create(#←ChatCompletionではなく、Completionを使っている
    model="gpt-3.5-turbo-instruct",  
    prompt="今日の天気がとても良くて、気分が",  #←promptを指定
    stop="。",  #←文字が出現したら文章を終了する
    max_tokens=100,  #←最大のトークン数
    n=2,  #←生成する文章の数
    temperature=0.5  #←多様性を表すパラメータ
    )

print(response)
