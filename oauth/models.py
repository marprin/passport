from django.db import models
from django.utils import timezone
from datetime import timedelta


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    client_key = models.CharField(max_length=255, unique=True)
    secret_key = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(max_length=1, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def find_active_client(client_key):
        return Client.objects.get(client_key=client_key, active=True)

    class Meta:
        indexes = [
            models.Index(fields=["client_key", "active"]),
            models.Index(fields=["secret_key", "active"]),
        ]


class IPAddress(models.Model):
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    ip_address = models.CharField(max_length=50)
    revoked = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name

    def is_authorized_ipaddress(self, ip_address):
        return self.ip_address == ip_address and revoked == False

    class Meta:
        indexes = [
            models.Index(fields=["ip_address", "revoked"]),
        ]


class Grant(models.Model):
    code = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=(timezone.now() + timedelta(minutes=5)))

    def __str__(self):
        return self.code

    def get_user_by_valid_grant_code(code, client):
        return Grant.objects.filter(
            code=code, client=client, revoked=False, expired_at__lte=timezone.now()
        ).first()

    class Meta:
        indexes = [
            models.Index(fields=["code", "client", "revoked", "expired_at"]),
        ]


class AccessToken(models.Model):
    access_token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    refresh_token = models.CharField(max_length=255, unique=True)
    expired_at = models.DateTimeField(null=True)
    is_refresh_token_used = models.BooleanField(max_length=1, default=False)
    revoked = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.access_token

    def find_by_access_token(access_token):
        return AccessToken.objects.filter(access_token=access_token)

    def find_valid_token_by_access_token(access_token):
        return (
            AccessToken.objects.filter(access_token=access_token)
            .filter(revoked=False)
            .filter(expired_at__gte=timezone.now())
            .first()
        )


class Verification(models.Model):
    reference_number = models.CharField(max_length=255, unique=True)
    otp = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    is_used = models.BooleanField(max_length=1, default=False)
    expired_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference_number

    def get_user_on_verification(reference_number, otp, client):
        now = timezone.now()

        return Verification.objects.filter(
            reference_number=reference_number,
            otp=otp,
            client=client,
            is_used=False,
            expired_at__lte=now,
        ).first()

    class Meta:
        indexes = [
            models.Index(
                fields=["reference_number", "otp", "client", "is_used", "expired_at"]
            ),
        ]
