import json

DEBANK_API_URL = 'https://api.debank.com'


def retry_request(time: int, wait: int):
    def decorator(func):
        from tenacity import retry, stop_after_attempt, wait_fixed

        @retry(stop=stop_after_attempt(time), wait=wait_fixed(wait))
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f'API request failed with status code: {response.status_code}')

        return wrapper

    return decorator


@retry_request(time=3, wait=5000)
def get(url: str, params: dict = None):
    import requests
    response = requests.get(url, params=params)
    return response


def get_balance_data(user_id: str):
    url = f'{DEBANK_API_URL}/token/cache_balance_list'
    data = get(url, params={'user_addr': user_id})
    return data


def get_project_data_by_user(user_id: str):
    url = f'{DEBANK_API_URL}/portfolio/project_list'
    data = get(url, params={'user_addr': user_id})
    return data
