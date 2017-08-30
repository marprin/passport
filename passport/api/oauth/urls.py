from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
]