from pottery.core.exceptions import BaseError


class AccountBaseError(BaseError):
    pass


class PhoneNumberRequiredError(AccountBaseError):

    message = 'Phone number must be set'


class PasswordRequiredError(AccountBaseError):

    message = 'Password must be set'


class SuperUserAttributeError(AccountBaseError):

    message = 'Superuser must have is_superuser=True'


class StaffUserAttributeError(AccountBaseError):

    message = 'Superuser must have is_staff=True.'
