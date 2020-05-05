from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, unique=True)
    pp_path = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
        ]


class LoginEvent(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
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
