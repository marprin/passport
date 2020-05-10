from django.urls import path
from . import views


app_name = "oauth"
urlpatterns = [
    path("login", views.OauthLoginView.as_view(), name="index"),
    path("verify/<slug:reference>", views.VerificationView.as_view(), name="verify"),
]
