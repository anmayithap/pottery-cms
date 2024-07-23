from http import HTTPStatus
from typing import Collection, Final, Self

from django.conf import settings
from urllib3 import PoolManager
from urllib3.exceptions import MaxRetryError, TimeoutError
from urllib3.response import BaseHTTPResponse
from urllib3.util.retry import Retry

from pottery.core.exceptions import HTTPAdapterMaxRetryError, HTTPAdapterTimeoutError


class HTTPAdapter:

    def __init__(self: Self) -> None:
        self._RETRIES_CODES: Final[Collection[int]] = [
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.GATEWAY_TIMEOUT,
            ]
        self._retries = Retry(
            total=settings.HTTP_RETRIES_COUNT,
            backoff_factor=settings.HTTP_RETRIES_OFFSET,
            status_forcelist=self._RETRIES_CODES,
        )
        self._http = PoolManager(num_pools=settings.HTTP_NUM_POOLS, retries=self._retries)

    def get(
        self: Self,
        url: str,
        fields: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> BaseHTTPResponse:
        try:
            response = self._http.request('GET', url, fields=fields, headers=headers)
        except MaxRetryError as exc:
            raise HTTPAdapterMaxRetryError(url=url) from exc
        except TimeoutError as exc:
            raise HTTPAdapterTimeoutError(url=url) from exc

        return response

    def post(
        self: Self,
        url: str,
        data: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> BaseHTTPResponse:
        try:
            response = self._http.request('POST', url, json=data, headers=headers)
        except MaxRetryError as exc:
            raise HTTPAdapterMaxRetryError from exc
        except TimeoutError as exc:
            raise HTTPAdapterTimeoutError from exc

        return response
