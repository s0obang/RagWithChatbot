from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm.invoke("Hello, world!")


import bs4
from langchain import hub
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import Prompt
import bs4
from langchain.schema import Document


#input_file = "/Users/minseon/2025/학부연구생/RAG/RagWithChatbot/output_data.json" 
input_file = "C:\Soop\연구\RagTest\ChatBotWithRag\output_data.json" 

with open(input_file, "r", encoding="utf-8") as f:
    text_content = f.read()

# 텍스트를 Document 리스트로 변환
docs = [Document(page_content=text_content)]

# 텍스트를 청크(Chunk)로 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=250)
splits = text_splitter.split_documents(docs)

# 벡터스토어 생성 (FAISS + OpenAI Embeddings)
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

print(f" Number of vectors stored: {vectorstore.index.ntotal}")


prompt = Prompt.Prompt.prompt7

llm = ChatOpenAI(model_name="o1-mini")
#o1 mini는 temp못씀

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

query = "요즘 운동이 취미인데 무슨 동아리를 하면 좋을까?"
answer = "".join(rag_chain.stream(query))
#normal_answer = llm.invoke(query).content

print(f"질문: {query}\n")
print(f"rag 답변: {answer}\n")
#print(f"일반 답변: {normal_answer}")

