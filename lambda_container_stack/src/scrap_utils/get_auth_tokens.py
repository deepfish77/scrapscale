import os
from selenium_driverless import webdriver
from selenium_driverless.scripts.network_interceptor import (
    NetworkInterceptor,
    InterceptedRequest,
)
import asyncio


async def on_request(
    data: InterceptedRequest, auth_container: dict, method: str = "GET"
):
    # Intercept GET requests
    if data.request.method == method:
        try:
            auth_header = data.request.headers.get("Authorization")
            if auth_header:
                # Append this auth header to the list in the container
                auth_container.setdefault("auth", []).append(auth_header)
                # print("Found auth header:", auth_header)
        except KeyError:
            print("No 'Authorization' header found in this request.")


async def get_auth_tokens(url, method="GET"):
    # Use a mutable container (dictionary) to store all auth tokens.
    auth_container = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # Uncomment and set your proxy if needed:
    # options.single_proxy = os.getenv("mobileproxy")

    async with webdriver.Chrome(options=options) as driver:
        # Pass the auth_container to the on_request callback using a lambda
        async with NetworkInterceptor(
            driver, on_request=lambda data: on_request(data, auth_container, method)
        ):
            await driver.get(url=url)
            # Wait for a few seconds to allow network requests to be made
            await driver.sleep(3)

    # Return the list of auth headers from the container (or None if not found)
    return auth_container.get("auth")


def get_token_for_url(url):
    # Run the asynchronous main function and return the collected auth headers.
    auth_tokens = asyncio.run(get_auth_tokens(url))

    unique = list(set(auth_tokens))
    filtered = [item for item in unique if "undefined" not in item]
    # print("Returned auth tokens:", filtered)
    return filtered


# # Replace with your target URL
# print(get_token_for_url("https://example.cne.gob.ec/resultados"))
