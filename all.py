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

'''
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


docs_frag = [extract_clean_text(doc.page_content) for doc in docs]

# 순수 텍스트 리스트-> Document 리스트 바꾼느거
docs_frag_documents = [Document(page_content=text) for text in docs_frag]

print(f"문서의 수: {len(docs)}")
print(docs_frag_documents)


if not docs_frag_documents:
    raise ValueError("📌 오류: 문서가 비어 있습니다. 데이터를 확인하세요.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

splits = text_splitter.split_documents(docs)
splits_frag = text_splitter.split_documents(docs_frag_documents)

'''
if not splits_frag:
    raise ValueError("📌 오류: 문서 분할 후에도 데이터가 없습니다.")
'''

# 벡터스토어 생성.
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

vectorstore_frag = FAISS.from_documents(documents=splits_frag, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()

print(f"Number of vectors stored: {vectorstore.index.ntotal}")
print(f"Number of vectors stored: {vectorstore_frag.index.ntotal}")

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    """당신은 질문-답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다. 당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
검색된 다음 문맥(context) 을 사용하여 질문(question) 에 답하세요. 만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 문맥과 상관없이 알아서 적당히 대답하세요. 당신이 모든 것을 알고있는 것 처럼 대답하세요. 주어진 문맥에 대한 언급을 하지 마세요
한글로 답변해 주세요. 단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.

#Question:
{question}

#Context:
{context}

#Answer:"""
)
prompt2 = PromptTemplate.from_template(
    """당신은 똑똑하고 논리적인 AI 어시스턴트입니다. 주어진 문맥(context)을 참고하여 질문(question)에 답하세요.

만약 문맥에서 직접적인 답을 찾을 수 없다면, 다음과 같은 방법을 사용하여 답변하세요:
1. **관련된 개념을 확장하여 설명**합니다.
2. **일반적인 지식**을 바탕으로 가능한 답변을 제공합니다.
3. **비슷한 맥락의 정보**를 활용하여 유사한 질문에 대한 답을 추론합니다.

단, 확실하지 않은 정보는 `정확한 답변을 위해 추가 정보가 필요할 수 있습니다.`라고 명시하세요.

### 질문:
{question}

### 문맥:
{context}

### 답변:
"""
)

prompt3 = PromptTemplate.from_template(
    """당신은 논리적이고 창의적인 AI 어시스턴트입니다. 당신의 임무는 **주어진 문맥(context)과 일반적인 지식을 활용하여 질문(question)에 대한 최선의 답을 제공하는 것**입니다.

**답변 규칙:**
1. 문맥에서 **직접적인 정보**가 있으면 이를 바탕으로 답하세요.
2. 문맥이 부족하면 **비슷한 개념이나 관련 정보를 활용하여 유추**하세요.
3. 문맥과 무관한 일반적인 지식이라도 **질문에 도움이 될 수 있다면 포함**하세요.
4. 확실하지 않은 정보는 `이 답변은 일반적인 정보에 기반한 것이므로 추가적인 검토가 필요합니다.`라고 표시하세요.

### 질문:
{question}

### 문맥:
{context}

### 답변:
"""
)

llm = ChatOpenAI(model_name="gpt-4o", temperature=0)


# 체인 생성
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


answer = "".join(rag_chain.stream(" 성신여자대학교 교내식당 3의 위치를 알려줘."))
print(answer)