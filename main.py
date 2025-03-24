from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import Prompt
from langchain.schema import Document
import os
import json

def write(resultPath, resultSet):
    #기존 텍스트 파일 읽기 (있으면 기존 내용 유지)
    if os.path.exists(resultPath):
        with open(resultPath, "r", encoding="utf-8") as f:
            existing_data = f.read()
    else:
        existing_data = ""

    #새로운 데이터 추가
    with open(resultPath, "w", encoding="utf-8") as f:
        f.write(existing_data)
        for line in resultSet:
            f.write(line)

    print(f"변환 완료 결과 저장됨: {resultPath}")

def test(questionPath, resultPath, rag_chain):
    # 질문 파일 읽기(공백 제거,한 줄씩 리스트로 저장)
    with open(questionPath, "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]  #빈 줄 제거

    results = []

    for idx, query in enumerate(questions, start=1):
        print(f"[{idx}] 질문 처리 중: {query}")
        answer = "".join(rag_chain.stream(query))
        result_entry = f"[질문 {idx}]\n{query}\n\n[답변]\n{answer}\n\n{'='*50}\n\n"
        results.append(result_entry)

    # 결과 저장
    write(resultPath, results)

def load_json_to_documents(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for item in data:
        title = item.get("title", "")
        content = item.get("content", "")
        comments = "\n".join(item.get("comments", []))
        create = item.get("create", "")

        full_text = f"{title}\n\n{content}\n\n답변:\n{comments}"
        documents.append(Document(page_content=full_text, metadata={"create": create}))
    
    return documents

# API 키 정보 로드
load_dotenv()


#input_file = "/Users/minseon/2025/학부연구생/RAG/RagWithChatbot/output_data.json" 
input_file = r"C:\Soop\연구\RagTest\ChatBotWithRag\output_data.json" 
#input_file = "/Users/soop/s0obang/학부연구생24w/RagWithChatbot/output_data.json"

docs = load_json_to_documents(input_file)


# 텍스트를 청크(Chunk)로 분할
#text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#splits = text_splitter.split_documents(docs)

# 벡터스토어 생성 (FAISS + OpenAI Embeddings)
vectorstore = FAISS.from_documents(documents=docs, embedding=OpenAIEmbeddings())
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
#questionPath = "/Users/soop/s0obang/학부연구생24w/RagWithChatbot/questions.txt"
#resultPath = "/Users/soop/s0obang/학부연구생24w/RagWithChatbot/results/result1"

questionPath = r"C:\Soop\연구\RagTest\ChatBotWithRag\questions.txt"
resultPath = r"C:\Soop\연구\RagTest\ChatBotWithRag\results/resultWithOutCustom"

test(questionPath, resultPath, rag_chain)


'''
너 질문 바꾸고 돌려볼때는 이부분 풀고, test 주석 처리하고 돌려보렴!!!!! 꼭 test주석해줘 우리 거지된다
query = "요즘 운동이 취미인데 무슨 동아리를 하면 좋을까?"
answer = "".join(rag_chain.stream(query))
#normal_answer = llm.invoke(query).content

print(f"질문: {query}\n")
print(f"rag 답변: {answer}\n")
#print(f"일반 답변: {normal_answer}")
'''







