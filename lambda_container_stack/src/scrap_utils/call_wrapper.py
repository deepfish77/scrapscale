import time
import functools
import requests
from retrying import retry


def rate_limited(min_interval: float):
    """
    Decorator to enforce a minimum interval (in seconds) between calls.
    """

    def decorator(func):
        last_called = [0.0]  # use a mutable container to store last call time

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            sleep_time = min_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result

        return wrapper

    return decorator


def execute_get_call(
    url: str, header: dict, params: dict = None, timeout: float = 10
) -> requests.Response:

    params = params or {}
    try:
        response = requests.get(url, headers=header, params=params, timeout=timeout)
        print("api_response.status_code:", response.status_code)
        response.raise_for_status()
        return response
    except requests.HTTPError as e:
        status_code = response.status_code if response is not None else None
        if status_code == 416:
            print("There are too many records")
        elif status_code and 400 <= status_code < 500:
            print("Bad Request")
        elif status_code and status_code >= 500:
            print("Server error")
        else:
            print("Something unusual happened")
        raise e
    except requests.Timeout as e:
        print("Timeout")
        raise e


# @rate_limited(3, 5)
@rate_limited(1.0)  # ensures at least 1 second between requests
@retry(wait_exponential_multiplier=1000, wait_exponential_max=32000)
def execute_get_call_with_retries(
    url: str, header: dict, params: dict = None
) -> requests.Response:

    return execute_get_call(url, header, params)
