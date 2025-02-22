import json
import time
import tls_client
import asyncio
import aioredis
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)
from requests.exceptions import HTTPError, Timeout, RequestException

# Redis configuration
REDIS_HOST = "localhost"  # Update with your Redis server address
REDIS_PORT = 6379
RATE_LIMIT = 5  # Maximum requests
RATE_PERIOD = 10  # Time window in seconds


# Initialize Redis connection
async def get_redis_connection():
    return await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")


# Redis-based rate limiter
async def is_rate_limited(redis, key):
    current_time = int(time.time())
    window_start = current_time - RATE_PERIOD

    # Remove expired requests from the sorted set
    await redis.zremrangebyscore(key, 0, window_start)

    # Get the count of requests in the current window
    request_count = await redis.zcard(key)

    if request_count >= RATE_LIMIT:
        return True

    # Add the new request to the sorted set with the current timestamp as the score
    await redis.zadd(key, {str(current_time): current_time})
    return False


# Exponential Backoff with retry logic
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((HTTPError, Timeout, RequestException)),
)
async def make_request(
    session, method, url, headers=None, data=None, json=None, proxies=None, params=None
):
    try:
        response = getattr(session, method.lower())(
            url,
            headers=headers,
            data=data,
            json=json,
            proxies=proxies,
            params=params,
            timeout=10,
        )
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        return (
            response.json()
            if "application/json" in response.headers.get("Content-Type", "")
            else response.text
        )

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Timeout as e:
        print(f"Request timed out: {e}")
    except RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


# Main function to execute the request with rate limiting and proxy support
async def execute_request_with_proxy(
    url, method="GET", headers=None, data=None, json=None, params=None, proxy=None
):
    redis = await get_redis_connection()
    session = tls_client.Session(
        client_identifier="chrome_112", random_tls_extension_order=True
    )

    request_key = f"rate_limit:{url}"

    # Check rate limiting using Redis
    if await is_rate_limited(redis, request_key):
        print("Rate limit exceeded. Please try again later.")
        return None

    proxies = {"http": proxy, "https": proxy} if proxy else None

    # Make the API request with retries and rate limiting
    response = await make_request(
        session=session,
        method=method,
        url=url,
        headers=headers,
        data=data,
        json=json,
        proxies=proxies,
        params=params,
    )

    await redis.close()
    return response


# Example usage
async def main():
    url = "https://example.com/api/data"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Authorization": "Bearer YOUR_API_TOKEN",
    }
    proxy = "http://your.proxy:port"

    response = await execute_request_with_proxy(
        url, method="GET", headers=headers, proxy=proxy
    )
    print("Response:", response)


# Run the asynchronous main function
asyncio.run(main())
