from django.db import models


class Client(models.Models):
    name = models.CharField(max_length=100, unique=True)
    public_key = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=100, unique=True)
    callback_url = models.CharField(max_length=255)
    active = models.BooleanField(max_length=1, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class IPAddress(models.Model):
    client = models.ForeignKey('oauth.Client')
    ip_address = models.CharField(max_length=50)
    revoked = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name


class Grant(models.Model):
    code = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey('oauth.Client')
    user = models.ForeignKey('user.User')
    ip_address = models.CharField(max_length=50)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True)   

    def __str__(self):
        return self.code


class AccessToken(models.Model):
    access_token = models.CharField(max_length=150, unique=True)
    user = models.ForeignKey('user.User')
    client = models.ForeignKey('oauth.Client')
    refresh_token = models.CharField(max_length=150, unique=True)
    expired_at = models.DateTimeField(null=True)
    is_refresh_token_used = models.BooleanField(max_length=1, default=False)
    revoked = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

