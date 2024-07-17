from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MasterClassConfig(AppConfig):
    name = 'pottery.master_class'
    verbose_name = _('Master class')
