from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()


class AuthenticationForm(forms.Form):
    phone_number = PhoneNumberField(
        label='Номер телефона',
        required=True,
    )
    password = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(),
    )
