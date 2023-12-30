from django.urls import path
from .views import Products_show

urlpatterns = [
    path('', Products_show.as_view(), name='base')
]