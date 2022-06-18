from django.urls import path,include
from rest_framework import routers
from . import views

urlpatterns = [
    path(
        'api/get/',
        views.GetOcr.as_view(),
        name='cls-v'),
]
