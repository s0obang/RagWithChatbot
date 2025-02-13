from bs4 import BeautifulSoup
import json
import random
import os

# 샘플 URL 생성 함수 (임시 URL)
def generate_dummy_urls(count):
    return [f"https://example.com/{random.randint(1000, 9999)}" for _ in range(count)]

# 파일에서 HTML 데이터 읽기
input_file = "input_data.txt"  # HTML 데이터가 있는 파일
output_file = "output_data.json"  # 변환된 JSON 데이터를 저장할 파일

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

        # 첨부 이미지 추출 (attaches 내의 이미지만)
        attach_images = article.find("div", class_="attaches")
        if attach_images:
            image_urls = [img["src"] for img in attach_images.find_all("img")]
        else:
            image_urls = generate_dummy_urls(1)  # 기본 더미 URL 추가

        # 댓글 추출
        comments = [comment.text.strip() for comment in article.find_all("p", class_="large")][1:]

        # JSON 형태의 데이터 추가
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

print(f"변환 완료! JSON 데이터가 {output_file}에 저장되었습니다.")
