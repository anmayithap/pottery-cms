from django.contrib.postgres import indexes
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from pottery.core.models import BaseModel
from pottery.master_class.choices import Status


class Client(BaseModel):
    first_name = models.CharField('Имя', max_length=32)

    phone_number = PhoneNumberField('Номер телефона')

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

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
    name = models.CharField('Название', max_length=128)
    visits = models.SmallIntegerField('Количество посещений')

    class Meta:
        db_table = 'program'
        verbose_name = 'Программа мастер-класса'
        verbose_name_plural = 'Программы мастер-классов'


class Visit(BaseModel):
    client = models.ForeignKey(
        'master_class.Client',
        on_delete=models.PROTECT,
        related_name='client_visits',
    )
    master = models.ForeignKey(
        'account.User',
        on_delete=models.PROTECT,
        related_name='master_visits',
    )
    program = models.ForeignKey(
        'master_class.Program',
        on_delete=models.PROTECT,
        related_name='program_visits',
    )
    work_piece = models.ForeignKey(
        'master_class.WorkPiece',
        on_delete=models.PROTECT,
        related_name='work_piece_visits',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'visit'
        verbose_name = 'Визит мастер-класса'
        verbose_name_plural = 'Визиты мастер-классов'


class WorkPiece(BaseModel):
    photo = models.ForeignKey(
        'master_class.Photo',
        on_delete=models.PROTECT,
        related_name='work_pieces',
    )
    status = models.CharField(
        'Статус изделия',
        max_length=16,
        choices=Status,
        default=Status.NEW,
    )
    is_glazed = models.BooleanField('Покрыто глазурью', default=False)
    expire_date = models.DateTimeField(
        'Дата просрочки',
        null=True,
        blank=True,
    )
    comment = models.TextField(
        'Примечание',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'work_piece'
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'

        indexes = (
            indexes.HashIndex(
                fields=('status',),
                name='work_piece__status__hash_index',
            ),
        )


class Photo(BaseModel):
    path = models.CharField('Путь к фото', max_length=248)

    class Meta:
        db_table = 'photo'
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
