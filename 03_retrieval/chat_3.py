import os
import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_text_splitters import SpacyTextSplitter
from langchain_chroma import Chroma


embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002"
)

chat = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(template="""文章を元に質問に答えてください。 

文章: 
{document}

質問: {query}
""", input_variables=["document", "query"])

text_splitter = SpacyTextSplitter(chunk_size=300, pipeline="ja_core_news_sm")

@cl.on_chat_start
async def on_chat_start():
    files = None #← ファイルが選択されているか確認する変数

    while files is None: #← ファイルが選択されるまで繰り返す
        files = await cl.AskFileMessage(
            max_size_mb=20,
            content="PDFを選択してください",
            accept=["application/pdf"],
            raise_on_timeout=False,
        ).send()
    file = files[0]

    msg = cl.Message(content=f"`{file.name}`を読み込み中です。しばらくお待ちください。") #← 読み込み中のメッセージを送信
    await msg.send()

    documents = PyMuPDFLoader(file.path).load() #← 保存したPDFファイルを読み込む
    splitted_documents = text_splitter.split_documents(documents) #← ドキュメントを分割する

    database = Chroma( #← データベースを初期化する
        embedding_function=embeddings,
        # 今回はpersist_directoryを指定しないことでデータベースの永続化を行わない
    )

    database.add_documents(splitted_documents) #← ドキュメントをデータベースに追加する

    cl.user_session.set(  #← データベースをセッションに保存する
        "database",  #← セッションに保存する名前
        database  #← セッションに保存する値
    )

    await cl.Message(content=f"`{file.name}`の読み込みが完了しました。質問を入力してください。").send() #← 読み込み完了を通知する

@cl.on_message
async def on_message(input_message):
    input_message = input_message.content
    print("入力されたメッセージ: " + input_message)

    database = cl.user_session.get("database") #← セッションからデータベースを取得する

    documents = database.similarity_search(input_message)

    documents_string = ""

    for document in documents:
        documents_string += f"""
    ---------------------------
    {document.page_content}
    """

    result = chat.invoke([
        HumanMessage(content=prompt.format(document=documents_string,
                                           query=input_message)) #← input_messageに変更
    ])
    await cl.Message(content=result.content).send()
