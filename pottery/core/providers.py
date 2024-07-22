from django.conf import settings
from urllib3 import PoolManager
from urllib3.exceptions import MaxRetryError, TimeoutError
from urllib3.response import HTTPResponse
from urllib3.util.retry import Retry

from pottery.core.exceptions import HTTPClientMaxRetryError, HTTPClientTimeoutError


class HTTPClient:
    def __init__(self):
        self.retries = Retry(
            total=5,
            backoff_factor=0.2,
            status_forcelist=[500, 502, 503, 504],
        )
        self.http = PoolManager(num_pools=5, retries=self.retries)

    def get(self, url: str, fields: dict = None, headers: dict[str, str] = None) -> HTTPResponse:
        try:
            response = self.http.request("GET", url, fields=fields, headers=headers)
        except MaxRetryError as exc:
            raise HTTPClientMaxRetryError(url=url) from exc
        except TimeoutError as exc:
            raise HTTPClientTimeoutError(url=url) from exc

        return response

    def post(self, url: str, data: str = None, headers: dict[str, str] = None) -> HTTPResponse:
        try:
            response = self.http.request("POST", url, json=data, headers=headers)
        except MaxRetryError as exc:
            raise HTTPClientMaxRetryError(url=url) from exc
        except TimeoutError as exc:
            raise HTTPClientTimeoutError(url=url) from exc

        return response


class YClientsProvider:
    def __init__(self, client: HTTPClient) -> None:
        self.client = client

    def auth(self) -> str:
        url = 'https://api.yclients.com/api/v1/auth'
        data = {'login': settings.YCLIENTS_LOGIN, 'password': settings.YCLIENTS_PASSWORD}
        headers = {
            'Authorization': f'Bearer {settings.YCLIENTS_BEARER_TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.api.v2+json"',
        }
        response = self.client.post(url, data, headers)
        user_token = response.json().get('data', {}).get('user_token', '')

        return user_token

    def get_records(self, pottery_id: int, user_token: str) -> dict:
        url = f'https://api.yclients.com/api/v1/records/{pottery_id}'
        headers = {
            'Authorization': f'Bearer {settings.YCLIENTS_BEARER_TOKEN}, User {user_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.api.v2+json',
        }
        response = self.client.get(url, headers=headers)
        return response.json().get('data', {})
