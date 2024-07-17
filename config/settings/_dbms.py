__all__ = (
    'DBMSConfig',
)

from typing import Literal, Self, TypeAlias, TypedDict

from config.settings._env_parse import Value

_PostgreSQLEngineAlias: TypeAlias = Literal['django.db.backends.postgresql']


class _DBMSConfig(TypedDict):
    ENGINE: _PostgreSQLEngineAlias
    NAME: str | Value[str]
    USER: str | Value[str]
    PASSWORD: str | Value[str]
    HOST: str | Value[str]
    PORT: str | Value[str]


class _DatabasesSetting(TypedDict):
    default: _DBMSConfig


class DBMSConfig:
    __slots__ = (
        '_name',
        '_user',
        '_password',
        '_host',
        '_port',
    )

    def __init__(
        self: Self,
        /,
        *,
        name: str | Value[str],
        user: str | Value[str],
        password: str | Value[str],
        host: str | Value[str],
        port: str | Value[str],
    ) -> None:
        self._name = name
        self._user = user
        self._password = password
        self._host = host
        self._port = port

    def to_dict(self: Self) -> _DatabasesSetting:
        return _DatabasesSetting(
            default=_DBMSConfig(
                ENGINE='django.db.backends.postgresql',
                NAME=self._name,
                USER=self._user,
                PASSWORD=self._password,
                HOST=self._host,
                PORT=self._port,
            ),
        )
