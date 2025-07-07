from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import DatetimeOutputParser  #← Output ParserであるDatetimeOutputParserをインポート
from langchain_core.messages import HumanMessage

output_parser = DatetimeOutputParser() #← DatetimeOutputParserを初期化

chat = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(
        template="{product}のリリース日を教えて。\n{format_instructions}",  #← format_instructionsをテンプレートに追加
        input_variables=["product"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()},  #← format_instructionsを追加
        )

result = chat.invoke(
    [
        HumanMessage(content=prompt.format(product="iPhone8")),  #← iPhone8のリリース日を聞く
    ]
)

output = output_parser.parse(result.content) #← 出力結果を解析して日時形式に変換する

print(output)
