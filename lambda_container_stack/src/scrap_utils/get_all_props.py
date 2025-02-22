import asyncio
import json
from selenium_driverless import webdriver


async def get_cookies(driver):
    """Return cookies as a list of dictionaries."""
    return await driver.get_cookies()


async def get_local_storage(driver):
    """Return the contents of window.localStorage as a dictionary."""
    local_storage_json = await driver.execute_script(
        "return JSON.stringify(window.localStorage);"
    )
    return json.loads(local_storage_json)


async def get_session_storage(driver):
    """Return the contents of window.sessionStorage as a dictionary."""
    session_storage_json = await driver.execute_script(
        "return JSON.stringify(window.sessionStorage);"
    )
    return json.loads(session_storage_json)


async def get_indexeddb(driver):
    """Return a list of IndexedDB databases, if supported."""
    script = """
    return new Promise((resolve, reject) => {
        if (indexedDB.databases) {
            indexedDB.databases().then(dbs => resolve(JSON.stringify(dbs))).catch(reject);
        } else {
            resolve("indexedDB.databases() not supported");
        }
    });
    """
    result = await driver.execute_script(script)
    try:
        return json.loads(result)
    except Exception:
        return result


async def get_cache_storage(driver):
    """Return a list of cache storage keys using the Cache API."""
    script = """
    return caches.keys().then(keys => JSON.stringify(keys));
    """
    result = await driver.execute_script(script)
    try:
        return json.loads(result)
    except Exception:
        return result


async def get_performance_metrics(driver):
    """Return the performance.timing metrics as a dictionary."""
    performance_json = await driver.execute_script(
        "return JSON.stringify(window.performance.timing);"
    )
    return json.loads(performance_json)


# Optional: If your driver supports retrieving console logs, you might implement:
async def get_console_logs(driver):
    """Return browser console logs if available (driver must support this)."""
    if hasattr(driver, "get_console_logs"):
        return await driver.get_console_logs()
    return None


async def get_all_properties(url):
    # Set up Chrome options in headless mode.
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    async with webdriver.Chrome(options=options) as driver:
        await driver.get(url=url)
        # Wait a few seconds for the page and its scripts to load
        await driver.sleep(3)

        cookies = await get_cookies(driver)
        local_storage = await get_local_storage(driver)
        session_storage = await get_session_storage(driver)
        indexed_db = await get_indexeddb(driver)
        cache_storage = await get_cache_storage(driver)
        performance_metrics = await get_performance_metrics(driver)
        console_logs = await get_console_logs(driver)

        print("Cookies:", cookies)
        print("Local Storage:", local_storage)
        print("Session Storage:", session_storage)
        print("IndexedDB:", indexed_db)
        print("Cache Storage:", cache_storage)
        print("Performance Metrics:", performance_metrics)
        print("Console Logs:", console_logs)


# asyncio.run(get_all_properties('target_url'))
