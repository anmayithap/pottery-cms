from typing import ParamSpec, Self

from django.db import models

_P = ParamSpec('_P')


class ActiveQuerySet(models.QuerySet):

    def filter(self: Self, *args: _P.args, **kwargs: _P.kwargs) -> Self:
        return super().filter(is_active=True).filter(*args, **kwargs)


class BaseModel(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)

    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего обновления', auto_now=True, blank=True, null=True)

    is_active = models.BooleanField('Активная запись?', default=True, db_index=True)

    objects = models.Manager()
    active_objects = ActiveQuerySet.as_manager()

    class Meta:
        abstract = True

    def __str__(self: Self) -> str:
        return f'{self.__class__.__name__}: {self.id}'
