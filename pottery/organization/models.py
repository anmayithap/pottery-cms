from django.db import models

from pottery.core.models import BaseModel


class City(BaseModel):
    name = models.CharField('Название', max_length=32, unique=True)

    class Meta:
        db_table = 'city'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Street(BaseModel):
    name = models.CharField('Название', max_length=128)

    city = models.ForeignKey(
        'organization.City',
        on_delete=models.PROTECT,
        related_name='streets',
        verbose_name='Город',
    )

    class Meta:
        db_table = 'street'
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'

        unique_together = ('name', 'city')


class Filiation(BaseModel):
    name = models.CharField('Название', max_length=128, unique=True)
    is_franchise = models.BooleanField('Франшиза?', default=False)

    street = models.OneToOneField(
        'organization.Street',
        on_delete=models.PROTECT,
        related_name='filial',
        verbose_name='Улица',
    )

    class Meta:
        db_table = 'filiation'
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'
