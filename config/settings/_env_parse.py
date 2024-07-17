import os
from typing import Any, Generic, Self, TypeVar

_T = TypeVar('_T', bound=Any)


class Value(Generic[_T]):

    def __new__(cls: type[Self], name: str, cast_to: type[Any] = str) -> _T:  # type: ignore[misc]
        value: str | None = os.environ.get(name)

        if value is None:
            raise ValueError(f'{name!r} does not found at environments variables...')

        try:
            casted_value: _T = cast_to(value)
        except TypeError as error:
            raise ValueError(f'Could not cast {name!r} from {type(value)!r} to {cast_to!r}') from error

        return casted_value
