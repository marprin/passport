from django.urls import path
from . import views


app_name = "oauth"
urlpatterns = [
    path("login", views.OauthLoginView.as_view(), name="index"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("verify/<slug:reference>", views.VerificationView.as_view(), name="verify"),
]
