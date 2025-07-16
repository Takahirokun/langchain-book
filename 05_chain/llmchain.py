from langchain_core.prompts import PromptTemplate  
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(  
    model="gpt-3.5-turbo",  
)

prompt = PromptTemplate(  
    template="{product}はどこの会社が開発した製品ですか？",  
    input_variables=[
        "product"  
    ]
)

chain = prompt | chat  #← ChatOpenAIとPromptTemplateをパイプでつなぐ


result = chain.invoke("iPhone8") #← Chainを実行する

print(result.content)
