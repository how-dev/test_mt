from django.urls import path

from .views import BaseLogin

urlpatterns = [
    path("login/", BaseLogin.as_view()),
]
