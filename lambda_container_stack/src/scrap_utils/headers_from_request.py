import os
import asyncio
from selenium_driverless import webdriver
from selenium_driverless.scripts.network_interceptor import (
    NetworkInterceptor,
    InterceptedRequest,
)


async def on_request(data: InterceptedRequest, container: dict, method: str = "GET"):
    """Intercepts network requests and stores relevant information in the container."""
    if data.request.method == method:
        try:
            # Capture Authorization header if present
            auth_header = data.request.headers.get("Authorization")
            if auth_header:
                container["Authorization"] = auth_header

            # Capture User-Agent header
            user_agent = data.request.headers.get("User-Agent")
            if user_agent:
                container["User-Agent"] = user_agent

            # Capture Referer header
            referrer = data.request.headers.get("Referer")
            if referrer:
                container["Referer"] = referrer

            # Capture Cookies header
            cookies = data.request.headers.get("Cookie")
            if cookies:
                container["Cookie"] = cookies

        except KeyError as e:
            print(f"KeyError during request interception: {e}")


async def collect_request_data(url: str, method: str = "GET") -> dict:
    """Launches a headless browser and collects headers and cookies from network requests."""
    container = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    async with webdriver.Chrome(options=options) as driver:
        async with NetworkInterceptor(
            driver, on_request=lambda data: on_request(data, container, method)
        ):
            await driver.get(url=url)
            await driver.sleep(3)

        # Get cookies from the browser
        cookies = driver.get_cookies()
        if cookies:
            container["Cookies"] = "; ".join(
                [f"{cookie['name']}={cookie['value']}" for cookie in cookies]
            )

    return container


def build_headers(url: str) -> dict:
    """Fetches request data and constructs the headers dictionary."""
    request_data = asyncio.run(collect_request_data(url))

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": request_data.get("Authorization", ""),
        "Cookie": request_data.get("Cookies", ""),
        "If-None-Match": 'W/"d2-qCAzSKDNrtLzCuacfnJESx6Ka4s"',
        "Priority": "u=1, i",
        "Referer": request_data.get("Referer", ""),
        "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": request_data.get("User-Agent", ""),
    }
    return headers


# Example usage:
url = "https://example.cne.gob.ec/resultados"
headers = build_headers(url)
print(headers)
