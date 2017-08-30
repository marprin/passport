from django.conf.urls import include, url
from .oauth import urls as oauth_url

urlpatterns = [
    url(r'^oauth/', include(oauth_url, namespace='oauth')),
]