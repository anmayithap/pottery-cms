# ruff: noqa: E501
from typing import Any, Final, Sequence

from config.settings.base import *  # noqa: F403
from config.settings.base import INSTALLED_APPS, MIDDLEWARE, WEBPACK_LOADER

DEBUG = True

ALLOWED_HOSTS: Final[Sequence[str]] = (
    '0.0.0.0',
    '127.0.0.1',
    'localhost',
)

INSTALLED_APPS = (
    'whitenoise.runserver_nostatic',
    *INSTALLED_APPS,
    'debug_toolbar',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG: Final[dict[str, Any]] = {
    'DISABLE_PANELS': (
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ),
    'SHOW_TEMPLATE_CONTEXT': True,
}

WEBPACK_LOADER['DEFAULT']['CACHE'] = not DEBUG

YCLIENTS_LOGIN = '79874977074'
YCLIENTS_PASSWORD = 'Fhctybq2001'
YCLIENTS_BEARER_TOKEN = 'Bearer um8bs2zydztepewb3hz8'
YCLIENTS_POTTERY_ID = 1085115
