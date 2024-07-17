from typing import ClassVar, ParamSpec

_P = ParamSpec('_P')


class BaseError(Exception):
    """Внутрення ошибка SDK.

    :cvar message: Базовое сообщение ошибки.
    :vartype message: str | None
    """

    message: ClassVar[str | None] = None

    def __init__(self, msg: str | None = None, **format: _P.kwargs) -> None:  # type: ignore[valid-type]
        message: str | None

        if msg:
            message = msg
        else:
            message = self.message

        if message:  # pragma: no cover
            message = message.format(**format)

        super().__init__(message)
