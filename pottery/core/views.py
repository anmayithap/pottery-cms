from typing import Any, Self

from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/index.html'
    extra_context = {
        'title': settings.TITLE,
        'description': settings.DESCRIPTION,
    }

    def get_context_data(self: Self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        kwargs['user'] = get_user(self.request)
        return super().get_context_data(**kwargs)
