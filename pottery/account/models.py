from typing import ClassVar, Final, Generic, Self, TypeVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as StandaloneUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres import indexes
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

_U = TypeVar('_U', bound='User')

_USERNAME_VALIDATOR: Final[UnicodeUsernameValidator] = UnicodeUsernameValidator()


class UserManager(Generic[_U], StandaloneUserManager):
    model: type[_U]


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Username'),
        max_length=128,
        unique=True,
        help_text=_('Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[_USERNAME_VALIDATOR],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )

    first_name = models.CharField(_('First name'), max_length=32)
    last_name = models.CharField(_('Last name'), max_length=32, blank=True, null=True)
    middle_name = models.CharField(_('Middle name'), max_length=32, blank=True, null=True)

    email = models.EmailField(_('Email'), unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(_('Phone number'), unique=True)

    filiations = models.ManyToManyField(
        'organization.Filiation',
        related_name='users',
        verbose_name=_('Filiations'),
    )

    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Is active?'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.',
        ),
    )
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    USERNAME_FIELD = 'username'

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

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
        return f'{self.__class__.__name__}: {self.username!s}'
