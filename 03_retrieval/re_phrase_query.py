from langchain_openai import ChatOpenAI
from langchain_community.retrievers import WikipediaRetriever
from langchain.retrievers import RePhraseQueryRetriever #← RePhraseQueryRetrieverをインポートする
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

retriever = WikipediaRetriever( 
    lang="ja", 
)
              
llm_chain = LLMChain( #← LLMChainを初期化する
    llm = ChatOpenAI( #← ChatOpenAIを指定する
        temperature = 0
    ),
    prompt = PromptTemplate( #← PromptTemplateを指定する
        input_variables=["question"],
        template="""以下の質問からWikipediaで検索するべきキーワードを抽出してください。
質問: {question}
"""
))

re_phrase_query_retriever = RePhraseQueryRetriever( #← RePhraseQueryRetrieverを初期化する
    llm_chain=llm_chain, #← LLMChainを指定する
    retriever=retriever, #← WikipediaRetrieverを指定する
)

documents = re_phrase_query_retriever.invoke("ところでバーボンウイスキーとは何ですか？")

print(documents)
