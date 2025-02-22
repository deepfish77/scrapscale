import requests
import json
from src.scrape.scrap_utils.get_auth_tokens import get_token_for_url
import pandas as pd
BASE_URL = "https://example.cne.gob.ec/resultados"
URL = "https://example.cne.gob.ec/certero/result/api/v1/total-provincias?codDignidad=12&codProvincia=0"
COOKIES = (
    "visid_incap_3187926=BQ5HvrmmRhG+kmbCRezPPkWttWcAAAAAQUIPAAAAAACySaZV8H5tJ6dboXX1x3Q/; "
    "incap_ses_1168_3187926=6HY5doJ/xQnkFtoHCpI1EEWttWcAAAAAV/QrutdY2voo3DUq6AC/Rg==; "
    "nlbi_3187926=9af4FWok33oF/dDLloXqmgAAAABKvdtIZACONRb4zrSF1quV; "
    "incap_wrt_1098=QrC1ZwAAAABjz2klGQAIyggQ+I3n3wIY7eLWvQYgAijG2ta9BjABlupsXrOfg9d4kXArlSXDCw=="
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
REFERRER = "https://example.cne.gob.ec/resultados"


def builde_headers(url, cookies, user_agent, referrer):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        f"Authorization": auth_bearer,
        "Cookie": cookies,
        "If-None-Match": 'W/"d2-qCAzSKDNrtLzCuacfnJESx6Ka4s"',
        "Priority": "u=1, i",
        "Referer": referrer,
        "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": user_agent,
    }
    return headers


auth_bearer = get_token_for_url(BASE_URL)[0]
headers = builde_headers(
    url=URL, cookies=COOKIES, user_agent=USER_AGENT, referrer=REFERRER
)
response = requests.get(URL, headers=headers)

print(response.status_code)
result = json.loads(response.text)

df = pd.DataFrame.from_dict(result.get("items"))
print(df.head)
df.to_csv('votos.csv')
