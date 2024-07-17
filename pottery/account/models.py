from typing import ClassVar, Generic, ParamSpec, Self, TypeVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as StandaloneUserManager
from django.contrib.postgres import indexes
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from pottery.account.exceptions import (
    PasswordRequiredError,
    PhoneNumberRequiredError,
    StaffUserAttributeError,
    SuperUserAttributeError,
)

_P = ParamSpec('_P')

_U = TypeVar('_U', bound='User')


class UserManager(Generic[_U], StandaloneUserManager):
    model: type[_U]

    def create_user(  # type: ignore[override,valid-type]
        self: Self,
        phone_number: str | None,
        password: str | None,
        **extra_fields: _P.kwargs,
    ) -> _U:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(  # type: ignore[override,valid-type]
        self,
        phone_number: str | None,
        password: str | None,
        **extra_fields: _P.kwargs,
    ) -> _U:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise StaffUserAttributeError
        if extra_fields.get('is_superuser') is not True:
            raise SuperUserAttributeError

        return self._create_user(phone_number, password, **extra_fields)

    def _create_user(  # type: ignore[valid-type]
        self: Self,
        phone_number: str | None,
        password: str | None,
        **extra_fields: _P.kwargs,
    ) -> _U:
        if not phone_number:
            raise PhoneNumberRequiredError
        if not password:
            raise PasswordRequiredError

        user: _U = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32, blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=32, blank=True, null=True)

    phone_number = PhoneNumberField(
        'Номер телефона',
        unique=True,
    )

    filiations = models.ManyToManyField(
        'organization.Filiation',
        related_name='users',
        verbose_name='Филиалы',
    )

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        indexes = (
            indexes.HashIndex(
                fields=('phone_number',),
                name='user__phone_number__hash_index',
            ),
            indexes.HashIndex(
                fields=('first_name',),
                name='user__first_name__hash_index',
            ),
        )

    def __str__(self: Self) -> str:
        return f'{self.__class__.__name__}: {self.phone_number!s}'
