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
    "recaptchaToken": "03AFcWeA481Cao68lVnO4LtmEql0IySkWHmr9xQ3f1_81LIsLlVothEjraXciSIu_ljCs5r4pElKq6NRnIHNxbujjbSctPIQcsj1sN_Vv1DFunvzdGBNh-0HUsnjytXKKIjMGsQmplJvwBhwqFGrMyPxpOxYeW3LZzViK0FP-X84JtfHC56VTkqNQwM0octEnaswevWWsdXtIP5K0JOeHRWRVPI7WywkmgeXHZtKL8Njsyn87zbxQsgmPtRhmXyRXWp2jiobiZexwbbtews_FZedBidoqE_UXfORjVyaYerctZ5A_Q6kdd1yYjwbueDyaSJU7uKz2QxesC3VM4dzTmGzIWn7e0ACb3j2kxxcdqLwkE2f0ggc9QYnCduOEhQoAOdIfvPkxkRAE_UQa-RaOx6abGiukxJqB6yxUgP32ELxYPKTXwQJlCVZW2jw1JGeGhYyKIX4_DtiXCC4yxSrEGNzQesmDEMGeMPkvp1CzX1QqagkI2d2qkkgr9gB4qod3Y80DkR46bvqEkg33gZL5y1u-2TrhCX_-QcDZ8_eyl_UPxtyfQsh59jL1NEr9443jl-0DsV83A3GzQZG5GEDK0xhLBzuzPq_WMWfSD-NRlnSgqJ25StCHoceB5wZn1dPDC0gkS9ybPdah0VqF4BeDGOrEGJtkp0ukknGMva6v1v-k1eHaGlkK6OWZeMrAEUbJofjHRIlY7zRiK7JAD3DhW1PBVClJrLQphRl8jRu-9Z0XfifTfMml9atgSgJ7jCB9JUeltLPrV3vy7vde42oV5OwAaYx5reDndq0Y-3zwhWqsYnYmUtGvV6X4-usOfpRp1YB6JnF_DwUKmsY8BUg7deqTvZCIUXW0SX8s64VY8L61HUGqsf-bJ04Pvin6PqdrfakRy7rKX3YZ4hqyrQ3n-r693G-qnfRNt2NElckZ45m93P-vWcdF_d497EYYLXlmY1p4jFj0I9hgc3Nbka0QtZsWvAnU5mGzqmfAsmRJ-hbGSTuAK7Ix0o4gvSfhBknKwlPiGsZKuzf5aMg2rgawjBPgiSg5g9t8OO5_3C-PBpui3hM13aF6GrkXd9kP82XMx9ItZ6kRyLdtRjGquUKZF6Vbo7gXZeh822s8Wmd-mnIqNXB4d1ZtDmKxgWh5vCX1H0LfU06DXHLAp1DsppPmeRUtM6qe0K-FQJ3zNg3gK8VYlDjcWMXk7Nr5dKX6l9jIGOaLzuTdLA6hKD6ubSJOXXQxJgQiPWEBSLPADVO0z-Z9VmFOhck8kmCa1jqL0gLGZE58dbHGdB1EAk_cKUiHO3NiXCW-c5zWGYt6t6No3IPgehI2hjEhnU25WYQVECRdxLBa_5WGp1Jdpg-XnBmxdb9lEfQH-9bz9hN8oPc8dZnHp8Oef1YIDSpaQzdo7gzZcP9cHZwJA2lHS9A5hPUM7pmgtylo3JvqtTyC0hyDkCtysN1LExvdMD3iZWWPWQ6Ft7ST_SNniSHRzpnib3ItFMJzN-EB0zxdRum_PqPxH591wyKfkjmdAYPf-hu-Nwdl5xP2V7h7_zHpBlzl03xMQAN-z6CRsMbkU3LeIuINm8atFtiulc592XDshw5Bcvy1us3AxnnWBUBmqPZyfKqWyHkC127yWadB_LghNhR2dQDDvTTPBkRUBBse1ABHs0HW1SrzdSNRX_g0wmDZvcCSBAg_EaxoYwIM52UVFDNoQXGuBbnQzusNIR6xk2Xmi_7EjVyWxHwZePiV-9IzZ-m0nU1CYvdMKCdfhdxxmSIFgKwPBAtPLL_bHIx_VKJGpyRP-2E7xJtWUqdS0TFHEmygyA8oorkDJ6403EPVXpfPEGHhw7H7c7T_l6ZVNhO7UVyv_PJhUTxt-bPU_aKb28BX6bGE4-r_jPvNF0geKk6TXN976U4F6QrJp-JSC7irz5bFBOJKmcQS3jgtAZXfV5Znb29YVfRPj1T07mmboq2K3IgE9LUvPSIujBDPtiIBCphMzifcHdVidh4qy"

}

# 4. 요청 헤더 설정 (개발자 도구에서 확인한 값 반영)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
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
