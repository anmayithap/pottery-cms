import logging
import os
from pathlib import Path
from typing import ParamSpec, Self

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

_P = ParamSpec('_P')

logger = logging.getLogger()


class Command(BaseCommand):

    def handle(self: Self, *args: _P.args, **options: _P.kwargs) -> None:
        current_environment = os.environ['DJANGO_SETTINGS_MODULE']

        logger.info(f'Start merging .env files for {current_environment!s}')

        if current_environment.rfind('.local') != -1:
            to_merge: Path = settings.BASE_DIR / '.environments' / '.local'
        elif current_environment.rfind('.prod') != -1:
            to_merge = settings.BASE_DIR / '.environments' / '.prod'
        else:
            raise CommandError(f'For environment {current_environment!s} does not exists .env files...')

        if not to_merge.exists():
            raise CommandError(f'Path {to_merge!s} does not exists...')

        content: str = ''

        for file in to_merge.glob('*.env'):
            if not file.is_file():
                continue

            logger.info(f'Inject to global .env environment variables from {file.name!s}')

            content += file.read_text()
            content += os.linesep

        content = content.rstrip()

        (settings.BASE_DIR / '.env').write_text(content)

        logger.info('Merging successfully')
