import requests
import json

# 1. 로그인 요청 URL
login_url = "https://account.everytime.kr/api/authenticate/login"

# 2. 세션 생성
session = requests.Session()

# 3. 로그인 데이터 설정 (`recaptchaToken` 필수 포함)
payload = {
    "id": "",  # 실제 아이디
    "password": "",  # 실제 비밀번호
    "keep": True,  # 로그인 유지 옵션
    "recaptchaToken": "03AFcWeA6YtDLQFnV3tO1XufDWoo1fluv4-yr7yraxhIqO11o_Xhz9M_J5Ev-J2jZuYuCGCvINwZm7AYh3X1GyHCiaMna4DsF_6PCfp2jqX5nV10Jtr6NEzrIeSfWM6OzK7_UMhEbn6KqRUkpUdeN8Ah_neWgbge6_MG4_HjXQpFixWEvM-jN4zz-JPxoG4-SVBUkiMKc-gYGpHuSuah_Cj57y21xQsiJhfcuu8im0uJXbt3URWg_5zXLQBDUVWVyeb6aaxZ_h5nZpw4MM57Q5dkMZ6J8ZT3p0nt5hpYBDBJimIlc2M0q2YyuBNxE6MUmq4urc5BeHhrCCUly3XgDmokGpwiAyj0BisPJy1nmMSZMWPay5FR9Foim4mn72NEtheAvudfb7bx6krT_R9gx5aziN13ABvEyvFuLSRuVJz1Sq6I3XjZVo1JpDHVSr_0AoQqn1Sjxrih3FnBvEqH3597WI4nvaBnMQAmti3JpzUI48-JZQH70-O3rx5RIbHdEhZkH-8r6jNfTphyzSksaZGYIIapOnwmDULpZE4nweEMgd8cEcNVDghTzaLgE1K2GpibAwTDq_7BNqSeJdzfKuCsYHzC7H373ohoS-n1mtJVLxatgmJZ9zmybpk-oChzVtmNp7iZ9b3FxGIz_7-OQMsXdnB7N4In_r4Yh5328-VYbGNbahvZKmhInFAzWv7MIhRbbQbLHGLkJ5u5UP4Pg56KlfbVCojfWb7XmuN6h-MPNQn7zXrN-8grlwnwt46WC-pdiR3xu5rnQ0Y7S1jYyqqzb1DerDVDkz-Y4n2poTKwPPWHhRC8KLHXEslthbNr-_ibjzqOohQqFydYxQkuv06zfRU9T6wi6GkXvkTgRHLzw3mnw5hf6CnoMwjpX-B4KjrSyOYGtKQQO-2Vp4BYsJ1MHGZ7AZH_e5Wj-rpp_lJtSaLooTJFX0BiEW443soTdX7GMBgyTVUu2i14mlhRWWl_o7SOUB6SFJLRaoFl4hyzaFGaxArG_af4D1w7mT4aKuFuEYZzlE-rJqYsRzcgVJL-0gDCTvMnjqDUrnQ4sF4dolTZyR7rjDTIVh2fmzemtKRAamFew37TGJi3riDUtvLQo8ufa-h1DLTKaX_j6qJ8Iw9LGHz8Y7S-pV1vjpjQKH6dsMzmQGQuV58RfIWfpjAeGIcc3hiiPGEwldCKVxaWqEU_ZZ2K9xyJNcvzb1Jyf0uSP85YssRpGvF3JvMQr2TV6-rMn8O3NcCwpjhjfL0p9KK-C3dgD4zJKjNUqMvY_c9K8Iy-OY3It1QfEs7JA2ww66SCS7DD9HgILBJV9dB4NB6m8bkcg_9IOFLToCIs_kShqgvKPR7HmkRXk3Mm0NKSH2k9uKQpNYM5OsJeCesULUjP6sm9GXTFFw3735m8iRdsuguSoc_y-PKd46z7rKrsINHTxKgWaknCjTTa6GLU-hcU5sMOUbwVIZT1NUlDDArtpG5pI14WmWbcIvtH6nLwV1ylqX8D9n2KRHbzLdoKK5VJV5jUYyA_bTigh-0-9Owz69rm8EvzRzjkXcQ_IO4zLVhk6GVvZaP4dUeeEXC-MskvrrfkPFYmpCzaSkURMd8XO-vbI2SPCzg3K2J23qrVEsQsn_mAghzW8CfAABSjQnozU58Whx0yRjzGlId92vdbjlHoB_91q-sf7UIelUxvW4g9QWg4Bbmm2hK50TFZ4hOwuMx9UszXOpkHNv9Jvr2p4amu7ut2gUtONHRkLO4R_nTI4xuKnL6qbIfxsmhf5xjYyLizs2HZNVhfFvL5T86_dxB1gzuNldGFo27dQVP4GCBRgpDUdJUNbV4FbDr6DegSDXGZ4dRpvRLHmLvncdmKN5BmeJii7J-5TZZJFJWPT8YyOjh2tHMaE2Lh3QMFVBzbVW2Fx-OWlGrQ1WgBGw8Q5GKBkw11q-fIItqF0D0u1QkmBkczBQAOutCbIvkGQqWEYTGJXcDRKoVNXlDLLEfYTR9s9esZLPFakVnMPSnxxceUw3-Fdm5A"  # 크롬 개발자 도구에서 복사한 reCAPTCHA 토큰
}

# 4. 요청 헤더 설정 (개발자 도구에서 확인한 값 반영)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Referer": "https://account.everytime.kr/",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://account.everytime.kr",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

# 5. 로그인 요청 실행 (JSON 데이터 전송)
response = session.post(login_url, data=json.dumps(payload), headers=headers)

# 6. 응답 데이터 출력
print("응답 상태 코드:", response.status_code)
print("응답 본문:", response.text)

# 7. 로그인 성공 시 쿠키 저장 확인
if response.status_code == 200:
    print("설정된 쿠키:", session.cookies.get_dict())
