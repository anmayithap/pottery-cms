# ruff: noqa: E501
from typing import Any, Final, Sequence

from config.settings.base import *  # noqa: F403
from config.settings.base import INSTALLED_APPS, MIDDLEWARE

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
