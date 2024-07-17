from django.contrib.postgres import indexes
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from pottery.core.models import BaseModel
from pottery.master_class.choices import Status


class Client(BaseModel):
    first_name = models.CharField(_('First name'), max_length=32)

    phone_number = PhoneNumberField(_('Phone number'), unique=True)

    class Meta:
        db_table = 'client'
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

        indexes = (
            indexes.HashIndex(
                fields=('phone_number',),
                name='client__phone__hash_index',
            ),
            indexes.HashIndex(
                fields=('first_name',),
                name='client__first_name__hash_index',
            ),
        )


class Program(BaseModel):
    name = models.CharField(_('Name'), max_length=128)
    visits = models.SmallIntegerField(_('Visits count'))

    class Meta:
        db_table = 'program'
        verbose_name = _('Master class program')
        verbose_name_plural = _('Master class programs')


class Visit(BaseModel):
    records = models.ManyToManyField(
        'master_class.Record',
        related_name='visits',
        verbose_name=_('Visit records'),
    )

    class Meta:
        db_table = 'visit'
        verbose_name = _('Master class visit')
        verbose_name_plural = _('Master class visits')


class Record(BaseModel):
    client = models.ForeignKey(
        'master_class.Client',
        on_delete=models.PROTECT,
        related_name='client_records',
        verbose_name=_('Enrolled client'),
    )
    master = models.ForeignKey(
        'account.User',
        on_delete=models.PROTECT,
        related_name='master_records',
        verbose_name=_('Selected master'),
    )
    program = models.ForeignKey(
        'master_class.Program',
        on_delete=models.PROTECT,
        related_name='program_records',
        verbose_name=_('Selected master class program'),
    )
    work_pieces = models.ManyToManyField(
        'master_class.WorkPiece',
        related_name='records',
        verbose_name=_('Record workpieces'),
        blank=True,
    )

    class Meta:
        db_table = 'record'
        verbose_name = _('Master class record')
        verbose_name_plural = _('Master class records')


class WorkPiece(BaseModel):
    photo = models.OneToOneField(
        'master_class.Photo',
        on_delete=models.PROTECT,
        related_name='workpiece',
        verbose_name=_('Photo'),
    )
    client = models.ForeignKey(
        'master_class.Client',
        on_delete=models.PROTECT,
        related_name='client_workpieces',
        verbose_name=_('Client'),
        blank=True,
        null=True,
    )
    master = models.ForeignKey(
        'account.User',
        on_delete=models.PROTECT,
        related_name='master_workpieces',
        verbose_name=_('Master'),
        blank=True,
        null=True,
    )
    status = models.CharField(
        _('Workpiece progress status'),
        max_length=16,
        choices=Status,
        default=Status.NEW,
    )
    is_glazed = models.BooleanField(_('Glazed?'), default=False)
    expire_date = models.DateTimeField(
        _('Expire date'),
        null=True,
        blank=True,
    )
    comment = models.TextField(
        _('Comment'),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'workpiece'
        verbose_name = _('Workpiece')
        verbose_name_plural = _('Workpieces')

        indexes = (
            indexes.HashIndex(
                fields=('status',),
                name='work_piece__status__hash_index',
            ),
        )


class Photo(BaseModel):
    path = models.CharField(_('Path to file'), max_length=248)

    class Meta:
        db_table = 'photo'
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
