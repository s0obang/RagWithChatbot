from bs4 import BeautifulSoup
import json
import random
import os
import boto3
import requests
from io import BytesIO
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 AWS 설정값 가져오기
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_FOLDER = os.getenv("S3_FOLDER")

# Boto3 S3 클라이언트 생성
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# HTML 파일 경로
input_file = "C:\Soop\연구\RagTest\ChatBotWithRag\input_club.txt"
output_file = "C:\Soop\연구\RagTest\ChatBotWithRag\output_club.json"  # 변환된 JSON 데이터를 저장할 파일

def download_and_upload_image(image_url):
    """이미지를 다운로드한 후 S3에 업로드하고 S3 URL 반환"""
    if not image_url:
        print("이미지 URL이 None. 업로드 건너뜀.")
        return None

    try:
        #이미지 다운
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            print(f"이미지 다운로드 실패: {image_url} (응답 코드: {response.status_code})")
            return None

        image_data = BytesIO(response.content)  # 메모리 내에서 파일처럼 다루기

        #파일 확장자 처리 (없으면 jpg)
        file_extension = image_url.split(".")[-1].split("?")[0] if "." in image_url else "jpg"
        s3_filename = f"{S3_FOLDER}{random.randint(1000, 9999)}.{file_extension}"  # S3 파일 경로 지정

        #S3에 업로드
        s3_client.upload_fileobj(image_data, S3_BUCKET_NAME, s3_filename, ExtraArgs={'ACL': 'public-read'})

        #업로드된 파일의 S3 URL 생성
        s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_filename}"
        print(f"이미지 업로드 성공: {s3_url}")
        return s3_url

    except Exception as e:
        print(f"이미지 업로드 중 오류 발생: {e}")
        return None

# HTML 데이터를 읽고 줄바꿈 기준으로 나눔
with open(input_file, "r", encoding="utf-8") as f:
    html_blocks = f.read().split("\n\n")  # 엔터(줄바꿈)로 구분된 HTML 블록

# JSON 결과 저장용 리스트
articles = []

# HTML 블록을 순회하며 파싱
for html_data in html_blocks:
    if not html_data.strip():  # 빈 줄은 무시
        continue

    soup = BeautifulSoup(html_data, "html.parser")

    # 게시물 데이터 추출
    for article in soup.find_all("article", class_="item"):
        title = article.find("h2", class_="large").text.strip()
        create_time = article.find("time", class_="large").text.strip()
        content = article.find("p", class_="large").text.strip()

        # 첨부 이미지 추출 (하나 또는 여러 개 처리)
        image_urls = []
        attach_images = article.find("div", class_="attaches")

        if attach_images:
            #이미지가 여러 개
            if "multiple" in attach_images.get("class", []):
                for img in attach_images.find_all("img"):
                    img_src = img.get("src")
                    if img_src:
                        print(f"다중 이미지 URL: {img_src}")
                        uploaded_url = download_and_upload_image(img_src)
                        if uploaded_url:
                            image_urls.append(uploaded_url)
                        else:
                            print(f"이미지 업로드 실패: {img_src}")

            #이미지 하나일경우
            elif "full" in attach_images.get("class", []):
                img_tag = attach_images.find("img")
                if img_tag:
                    img_src = img_tag.get("src")
                    if img_src:
                        print(f"단일 이미지 URL: {img_src}")
                        uploaded_url = download_and_upload_image(img_src)
                        if uploaded_url:
                            image_urls.append(uploaded_url)
                        else:
                            print(f"이미지 업로드 실패: {img_src}")
                else:
                    print("img없음. 업로드 건너뜀.")

        #댓글
        comments = [comment.text.strip() for comment in article.find_all("p", class_="large")][1:]

        # JSON 형태로 데이터 추가
        articles.append({
            "title": title,
            "create": create_time,
            "content": content,
            "imageUrls": image_urls,
            "comments": comments
        })

# 기존 JSON 파일 읽기 (파일이 존재하면 기존 데이터 유지)
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

# 새로운 데이터 추가 후 JSON 저장
existing_data.extend(articles)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"변환 완료")
