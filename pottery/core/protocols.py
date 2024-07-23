from typing import Protocol, Self

from urllib3.response import BaseHTTPResponse


class HTTPProtocol(Protocol):

    def get(self: Self, url: str, fields: dict[str, str] | None, headers: dict[str, str] | None) -> BaseHTTPResponse:
        ...

    def post(self: Self, url: str, data: dict[str, str] | None, headers: dict[str, str] | None) -> BaseHTTPResponse:
        ...
