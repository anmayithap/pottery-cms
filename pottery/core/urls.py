from django.urls import path

from pottery.core.views import IndexView

app_name: str = 'core'

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
)
