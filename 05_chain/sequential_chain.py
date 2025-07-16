from langchain.chains import SimpleSequentialChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

chat = ChatOpenAI(model="gpt-3.5-turbo")

# 記事を書くLLMChainを作成する
article_prompt = ChatPromptTemplate.from_template("{input}についての記事を書いてください。")
write_article_chain = article_prompt | chat

translate_prompt = ChatPromptTemplate.from_template(template="以下の文章を英語に翻訳してください。\n{input}")

# 翻訳するLLMChainを作成する 
translate_chain = {"input": write_article_chain} | translate_prompt | chat

result = translate_chain.invoke({"input": "エレキギターの選び方"})

print(result)
