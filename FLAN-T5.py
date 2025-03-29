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
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline


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

    print(f"변환 완료, 결과 저장됨: {resultPath}")

def test(questionPath, resultPath):
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


input_file = "/Users/minseon/2025/학부연구생/RAG/RagWithChatbot/output_data.json" 
#input_file = r"C:\Soop\연구\RagTest\ChatBotWithRag\output_data.json" 
#input_file = "/Users/soop/s0obang/학부연구생24w/RagWithChatbot/output_data.json"

docs = load_json_to_documents(input_file)

# 텍스트를 청크(Chunk)로 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

# 벡터스토어 생성 (FAISS + OpenAI Embeddings)
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})  #입력 토큰 터졌을 때 가져오는 문서 수 줄이려면 파라미터로 search_kwargs={"k": 3}

#prompt = Prompt.Prompt.prompt7
prompt = Prompt.Prompt.prompt_bart

'''
#bart
bart_pipe = pipeline(
    "text2text-generation",
    model="facebook/bart-large",
    tokenizer="facebook/bart-large",
    max_new_tokens=300,  # 출력 길이 조정
    device=-1
)
'''

kobart_pipe = pipeline(
    "text2text-generation",
    model="digit82/kobart-summarization",  # 또는 다른 KoBART
    tokenizer="digit82/kobart-summarization",
    max_new_tokens=300,
    device=-1
)


llm = HuggingFacePipeline(pipeline=kobart_pipe)
'''

flan_pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-xl",
    tokenizer="google/flan-t5-xl",
    max_new_tokens=500,
    device=-1 # apple 칩 내장 gpu에서는 토치 불안정해서 cpu로 돌리도록 설정
)

llm = HuggingFacePipeline(pipeline=flan_pipe)'
'''

# retriever가 문서 객체를 반환하므로, 문서 객체를 텍스트로 변환
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    prompt
    | llm
    | StrOutputParser()
)
#questionPath = "/Users/soop/s0obang/학부연구생24w/RagWithChatbot/questions.txt"
#resultPath = "/Users/soop/s0obang/학부연구생24w/RagWithChatbot/results/result1"

#questionPath = r"C:\Soop\연구\RagTest\ChatBotWithRag\questions.txt"
#resultPath = r"C:\Soop\연구\RagTest\ChatBotWithRag\results/resultWithOutCustom"

questionPath = "/Users/minseon/2025/학부연구생/RAG/RagWithChatbot/questions.txt"
resultPath = "/Users/minseon/2025/학부연구생/RAG/RagWithChatbot/results/resultWithOutCustom"

#test(questionPath, resultPath)

query = "이번 장학금 선감면이야?"
docs = retriever.invoke(query)
print(f"📄 문서 개수: {len(docs)}")
print(f"📄 문서 내용: {docs}")

if docs:
    context = format_docs(docs)
    inputs = {"question": query, "context": context}
    answer = rag_chain.invoke(inputs)
    if not answer.strip():
        answer = "문맥에서 관련된 내용을 찾지 못했어요. 더 구체적인 질문을 해볼래요?"
else:
    answer = "❌ 문맥에서 참고할 만한 정보를 찾지 못했어요. 다른 질문을 해줄래요?"

print(f"질문: {query}\n")
print(f"rag 답변: {answer}\n")