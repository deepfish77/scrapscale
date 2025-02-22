import asyncio
from selenium_driverless import webdriver
import json


async def get_cookies(url: str):
    # Set up Chrome options (headless mode)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Launch the browser using an asynchronous context manager
    async with webdriver.Chrome(options=options) as driver:
        # Navigate to the specified URL
        await driver.get(url=url)
        # Optionally, wait a few seconds for the page to fully load cookies
        await driver.sleep(3)
        # Retrieve cookies as a list of dictionaries
        cookies = await driver.get_cookies()
        print("Cookies:", cookies)
        return cookies


async def get_internal_storage(url: str):
    # Set up headless Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    async with webdriver.Chrome(options=options) as driver:
        await driver.get(url=url)
        # Wait for the page to load and localStorage to be populated
        await driver.sleep(3)

        # Retrieve the entire localStorage as a JSON string
        local_storage_json = await driver.execute_script(
            "return JSON.stringify(window.localStorage);"
        )
        # Parse the JSON string into a Python dictionary
        local_storage = json.loads(local_storage_json)
        print("Local Storage:", local_storage)
        return local_storage
