from django.urls import path
from . import views

urlpatterns = [
    path('', views.newton_raphson, name='solver'),
]