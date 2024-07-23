from datetime import datetime, timedelta
from typing import Any, Self

from django.conf import settings

from pottery.core.exceptions import HTTPAdapterMaxRetryError, HTTPAdapterTimeoutError
from pottery.core.protocols import HTTPProtocol


class YClientsProvider:
    """Провайдер для работы с внешним сервисом YClients."""

    def __init__(self: Self, client: HTTPProtocol) -> None:
        self._client = client

    def _build_headers(self: Self, user_token: str | None = None) -> dict[str, str]:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.api.v2+json',
        }
        if user_token:
            headers.update([('Authorization', f'Bearer {settings.YCLIENTS_BEARER_TOKEN}, User {user_token}')])
        else:
            headers.update([('Authorization', f'Bearer {settings.YCLIENTS_BEARER_TOKEN}')])

        return headers

    def _build_period(self: Self) -> str:
        if settings.YCLIENTS_TIME_PERIOD is None:
            raise ValueError('Не указан период времени')
        start_date = datetime.now() - timedelta(days=settings.YCLIENTS_TIME_PERIOD)

        return start_date.strftime('%Y-%m-%d')

    def auth(self: Self) -> Any:
        """Аутентификация пользователя и получение пользовательского токена."""
        url = 'https://api.yclients.com/api/v1/auth'
        data = {'login': settings.YCLIENTS_LOGIN, 'password': settings.YCLIENTS_PASSWORD}
        if data.get('login') is None or data.get('password') is None:
            raise ValueError('Не указаны логин или пароль')
        try:
            response = self._client.post(url=url, data=data, headers=self._build_headers())
        except (HTTPAdapterMaxRetryError, HTTPAdapterTimeoutError) as exc:
            raise exc

        user_token = response.json().get('data', {}).get('user_token', '')

        return user_token

    def get_records(self: Self, pottery_id: int, user_token: str) -> Any:
        """Получение всех записей."""
        url = f'https://api.yclients.com/api/v1/records/{pottery_id}'
        fields = {'start_date': self._build_period()}
        try:
            response = self._client.get(url, fields=fields, headers=self._build_headers(user_token))
        except (HTTPAdapterMaxRetryError, HTTPAdapterTimeoutError) as exc:
            raise exc

        return response.json().get('data', {})
