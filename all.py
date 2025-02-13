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
import os
import openai
import os
import Prompt

import bs4
from bs4 import BeautifulSoup
from langchain.schema import Document
import re

import requests
'''
# 1. 로그인 URL 후보
urls = [
    "https://everytime.kr/user/login",
    "https://everytime.kr/auth/login",
    "https://account.everytime.kr/login",
    "https://account.everytime.kr/authenticate"
]

# 2. 각 URL 확인
for url in urls:
    response = requests.get(url)
    print(f"URL: {url}, 상태 코드: {response.status_code}")


# 1. 로그인 URL과 로그인 데이터 설정
login_url = "https://account.everytime.kr/api/authenticate/login"
target_url = "https://everytime.kr/257604"

# 2. 세션 생성
session = requests.Session()

# 3. 로그인 데이터 (ID/PW 입력, 실제 필요한 데이터를 확인해야 함)
payload = {
    "id": "",
    
    "password": "",
    # 추가적인 hidden 필드나 토큰 값이 있다면 확인 후 추가해야 함
    "redirect_uri": "https://everytime.kr",
    "keep": "true"
}
#헤더 추가
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://everytime.kr/login",
    "Content-Type": "application/x-www-form-urlencoded"
}


# 4. 로그인 요청 보내기
response = session.post(login_url, data=payload, headers=headers, allow_redirects=False)

if "Set-Cookie" in response.headers:
    cookies = response.headers["Set-Cookie"]
    for cookie in cookies.split(";"):
        if "etsid=" in cookie:
            etsid_value = cookie.split("=")[1]
            session.cookies.set("etsid", "s%3Akuz_dlxg59Nwx2oYP8LrvRLpRjfB02gn.R%2FfRfoyKINFAcffnJeVkvABh9gCziIsPmKEFeScKHc", domain="everytime.kr")


login_url = "https://account.everytime.kr/api/authenticate/login"
target_url = "https://everytime.kr/257604"
session = requests.Session()
session.cookies.set("etsid", "s:kuz_dlxg59Nwx2oYP8LrvRLpRjfB02gn.R/fRfoyKINFAcffnJeVkvABh9gCziIsPmKEFeScKHc", domain="everytime.kr")
print("설정된 쿠키:", session.cookies.get_dict())




    

loader = WebBaseLoader(
    web_paths=(target_url,),
    session=session,  # 로그인된 세션을 WebBaseLoader에 전달
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            "h2",
            attrs={"class": ["medium bold"]},
        )
    ),
)

    # 7. 데이터 가져오기
docs = loader.load()
for doc in docs:
    print(doc.page_content)



#이부분 추가로 텍스트만 추출
def extract_clean_text(html_content):
    """
    - HTML 태그 제거
    - 불필요한 개행 문자 및 공백 제거
    """
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)  # 여러 개의 공백을 하나로 변환
    text = text.strip()

    return text

'''

# ✅ 1. TXT 파일에서 텍스트 로드
input_file = r"C:\Soop\연구\RagTest\ChatBotWithRag\output_data.json"  # TXT 파일 경로

with open(input_file, "r", encoding="utf-8") as f:
    text_content = f.read()

# ✅ 2. 텍스트를 Document 리스트로 변환
docs = [Document(page_content=text_content)]

# ✅ 3. 텍스트를 청크(Chunk)로 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# ✅ 4. 벡터스토어 생성 (FAISS + OpenAI Embeddings)
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

#print(f"📌 Number of vectors stored: {vectorstore.index.ntotal}")

# ✅ 5. 프롬프트 템플릿 정의
prompt = Prompt.Prompt.prompt4

# ✅ 6. LLM 설정 (GPT-4o 사용)
llm = ChatOpenAI(model_name="gpt-4o", temperature=1)

# ✅ 7. RAG 체인 생성
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ✅ 8. 질문 실행 (TXT 데이터 기반 검색)
query = "수룡이 인형 어디서 사?"
answer = "".join(rag_chain.stream(query))

# ✅ 9. 결과 출력
print(f"질문: {query}")
print(f"답변: {answer}")


#그냥 지피티 사용도 구현해놓기
#답변 걍 이어서 하게

