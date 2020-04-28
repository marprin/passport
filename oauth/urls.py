from django.urls import path
from . import views


app_name = 'oauth'
urlpatterns = [
    path('login', views.index, name='index'),
]