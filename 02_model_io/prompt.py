from langchain_core.prompts import PromptTemplate  #← PromptTemplateをインポート

prompt = PromptTemplate.from_template(  #← PromptTemplateを初期化する
    "{product}はどこの会社が開発した製品ですか？"  #← {product}という変数を含むプロンプトを作成する
)

print(prompt.invoke({"product": "Xperia"}))  #← invokeメソッドを使って変数に値を渡す
print(prompt.invoke({"product": "iPhone"}))  #← 別の値を渡してプロンプトを実行する
