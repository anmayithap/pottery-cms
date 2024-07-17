from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Status(TextChoices):
    NEW = 'NEW', _('New')
    IN_PROGRESS = 'IN_PROGRESS', _('In progress')
    READY = 'READY', _('Ready')
    GIVEN = 'GIVEN', _('Given')
    OVERDUE = 'OVERDUE', _('Overdue')
    BROKEN = 'BROKEN', _('Broken')
    REPEAT_VISIT = 'REPEAT_VISIT', _('Repeat visit')
