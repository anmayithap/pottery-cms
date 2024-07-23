from django.urls import path

from pottery.core.views import IndexView

app_name = 'core'

urlpatterns = (
    path('', view=IndexView.as_view(), name='index'),
)
