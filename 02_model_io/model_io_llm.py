from langchain_openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-instruct" #← 呼び出すモデルを指定
             )

result = llm.invoke(
    "美味しいラーメンを",  #← 言語モデルに入力されるテキスト
    stop="。"  #← 「。」が出力された時点で続きを生成しないように
)
print(result)
