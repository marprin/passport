from django.db import models
from django.conf import settings


class UserManager(models.Manager):
    def active(self):
        return self.filter(revoked=False)

    def not_reach_max_attempt(self):
        return self.filter(failed_login_attempt__lte=settings.MAX_FAILED_LOGIN_ATTEMPT)


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, unique=True)
    revoked = models.BooleanField(default=False)
    otp_email_enabled = models.BooleanField(default=False)
    failed_login_attempt = models.SmallIntegerField(default=0)
    pp_path = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.name

    def get_non_blocked_by_id(pk):
        return User.objects.active().not_reach_max_attempt().filter(pk=pk).first()

    def get_non_blocked_user(email):
        return User.objects.filter(email=email).active().not_reach_max_attempt().first()

    class Meta:
        indexes = [models.Index(fields=["email", "revoked", "failed_login_attempt"])]


class LoginEvent(models.Model):
    email = models.CharField(max_length=255)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    ip_address = models.CharField(max_length=50)
    platform = models.CharField(max_length=150)
    browser = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    action = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class Device(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    identifier = models.CharField(max_length=255, unique=True)
    ip_address = models.CharField(max_length=50)
    platform = models.CharField(max_length=150)
    browser = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    revoked = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
