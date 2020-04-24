from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, null=True)
    pp_path = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LoginEvent(models.Model):
    user = models.ForeignKey('user.User')
    client = models.ForeignKey('oauth.Client')
    ip_address = models.CharField(max_length=50)
    platform = models.CharField(max_length=150)
    browser = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    action = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class Device(models.Model):
    user = models.ForeignKey('user.User')
    client = models.ForeignKey('oauth.Client')
    ip_address = models.CharField(max_length=50)
    platform = models.CharField(max_length=150)
    browser = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    revoked = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
