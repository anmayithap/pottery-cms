from django.db import models
from django.utils.translation import gettext_lazy as _

from pottery.core.models import BaseModel


class City(BaseModel):
    name = models.CharField(_('Name'), max_length=32, unique=True)

    class Meta:
        db_table = 'city'
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Street(BaseModel):
    name = models.CharField(_('Name'), max_length=128)

    city = models.ForeignKey(
        'organization.City',
        on_delete=models.PROTECT,
        related_name='streets',
        verbose_name=_('City'),
    )

    class Meta:
        db_table = 'street'
        verbose_name = _('Street')
        verbose_name_plural = _('Streets')

        unique_together = ('name', 'city')


class Filiation(BaseModel):
    name = models.CharField(_('Name'), max_length=128, unique=True)
    is_franchise = models.BooleanField(_('Franchise?'), default=False)

    street = models.OneToOneField(
        'organization.Street',
        on_delete=models.PROTECT,
        related_name='filial',
        verbose_name=_('Street'),
    )

    class Meta:
        db_table = 'filiation'
        verbose_name = _('Filiation')
        verbose_name_plural = _('Filiations')
