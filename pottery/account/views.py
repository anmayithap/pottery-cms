from django.contrib.auth.views import LoginView as StandaloneLoginView


class LoginView(StandaloneLoginView):
    template_name = 'pages/login.html'

    redirect_authenticated_user = True
