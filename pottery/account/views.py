from django.views.generic import FormView

from pottery.account.forms import AuthenticationForm


class LoginView(FormView):

    form_class = AuthenticationForm
