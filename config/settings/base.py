# ruff: noqa: ERA001, E501
from pathlib import Path
from typing import Any, Final, Literal, Sequence

import dotenv
from psycopg import IsolationLevel

from config.settings._dbms import DBMSConfig
from config.settings._env_parse import Value

BASE_DIR: Final[Path] = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR: Final[Path] = BASE_DIR / 'pottery'

dotenv.load_dotenv(BASE_DIR / '.env')

# ==========> GENERAL SECTION

SECRET_KEY: Final[str] = Value('SECRET_KEY')  # type: ignore[assignment]

DEBUG: bool = False

TIME_ZONE: Final[str] = 'Europe/Moscow'

LANGUAGE_CODE: Final[str] = 'ru'

USE_I18N: Final[bool] = True

USE_TZ: Final[bool] = True

# ==========> DATABASES SECTION

DATABASES: Final[Any] = DBMSConfig(
    name=Value('DB_USER'),
    user=Value('DB_USER'),
    password=Value('DB_PASSWORD'),
    host=Value('DB_HOST'),
    port=Value('DB_PORT'),
).to_dict()

DATABASES['default']['CONN_HEALTH_CHECKS'] = True
DATABASES['OPTIONS'] = dict(
    isolation_level=IsolationLevel.READ_COMMITTED,
)

DEFAULT_AUTO_FIELD: Final[Literal['django.db.models.BigAutoField']] = 'django.db.models.BigAutoField'

# ==========> URLS ROUTE SECTION

ROOT_URLCONF: Final[Literal['config.urls']] = 'config.urls'
WSGI_APPLICATION: Final[Literal['config.wsgi.application']] = 'config.wsgi.application'

# ==========> APPS SECTION

STANDALONE_APPS: Final[tuple[str, ...]] = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.forms',
)

THIRD_PARTY_APPS: Final[tuple[str, ...]] = (
    'phonenumber_field',
    'crispy_forms',
    'crispy_bootstrap5',
    'webpack_loader',
)

LOCAL_APPS: Final[tuple[str, ...]] = (
    'pottery.core',
    'pottery.account',
    'pottery.organization',
    'pottery.master_class',
)

INSTALLED_APPS: tuple[str, ...] = STANDALONE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ==========> AUTHENTICATION SECTION

AUTHENTICATION_BACKENDS: Final[Sequence[str]] = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL: Final[Literal['account.User']] = 'account.User'

# ==========> PASSWORDS SECTION

PASSWORD_HASHERS: Final[Sequence[str]] = (
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)

AUTH_PASSWORD_VALIDATORS: Final[Sequence[dict[str, str]]] = (
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
)

# ==========> MIDDLEWARE SECTION

MIDDLEWARE: tuple[str, ...] = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# ==========> STATIC SECTION

STATIC_ROOT: Final[Path] = BASE_DIR / 'staticfiles'
STATIC_URL: Final[Literal['static/']] = 'static/'
STATICFILES_DIRS: Final[Sequence[Path]] = (
    APPS_DIR / 'static',
)
STATICFILES_FINDERS: Final[Sequence[str]] = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# ==========> MEDIA SECTION

MEDIA_ROOT: Final[Path] = APPS_DIR / 'media'
MEDIA_URL: Final[Literal['media/']] = 'media/'

# ==========> TEMPLATES SECTION

TEMPLATES: Final[Sequence[dict[str, Any]]] = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            APPS_DIR / 'templates',
        ),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ),
        },
    },
)

FORM_RENDERER: Final[Literal['django.forms.renderers.TemplatesSetting']] = 'django.forms.renderers.TemplatesSetting'

CRISPY_TEMPLATE_PACK: Final[Literal['bootstrap5']] = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS: Final[Literal['bootstrap5']] = 'bootstrap5'

# ==========> SECURITY SECTION

SESSION_COOKIE_HTTPONLY: Final[bool] = True
CSRF_COOKIE_HTTPONLY: Final[bool] = True
X_FRAME_OPTIONS: Final[Literal['DENY']] = 'DENY'

# ==========> LOGGING SECTION

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {'level': 'INFO', 'handlers': ['console']},
}

# ==========> WEBPACK SECTION

WEBPACK_LOADER: Final[dict[str, Any]] = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'STATS_FILE': BASE_DIR / 'webpack-stats.json',
        'POLL_INTERVAL': 0.1,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
    },
}
