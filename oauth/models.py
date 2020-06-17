from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class ClientQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(revoked=False)


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    client_key = models.CharField(max_length=255, unique=True)
    secret_key = models.CharField(max_length=255, unique=True)
    revoked = models.BooleanField(max_length=1, default=False)
    callback_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ClientQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["client_key", "revoked"]),
            models.Index(fields=["secret_key", "revoked"]),
        ]


class IPAddress(models.Model):
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    ip_address = models.CharField(max_length=50)
    revoked = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.name

    def is_authorized_ipaddress(ip_address):
        return IPAddress.objects.filter(ip_address=ip_address).filter(revoked=False)

    class Meta:
        indexes = [
            models.Index(fields=["ip_address", "revoked"]),
        ]

        unique_together = [["ip_address", "client"]]


class GrantQuerySet(models.query.QuerySet):
    def create_grant(self, *args, **kwargs):
        kwargs["expired_at"] = timezone.now() + timedelta(
            minutes=settings.GRANT_MINUTES_EXPIRED_MINUTES
        )
        return self.create(**kwargs)

    def active(self):
        return self.filter(revoked=False)

    def not_expired(self):
        return self.filter(expired_at__lte=timezone.now())


class Grant(models.Model):
    code = models.CharField(max_length=255)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()

    objects = GrantQuerySet.as_manager()

    def __str__(self):
        return self.code

    class Meta:
        indexes = [
            models.Index(fields=["code", "client", "revoked", "expired_at"]),
        ]

        unique_together = [["code", "client"]]


class AccessTokenQuerySet(models.query.QuerySet):
    def create_token(self, *args, **kwargs):
        kwargs["access_token_expired_at"] = timezone.now() + timedelta(
            days=settings.ACCESS_TOKEN_EXPIRED_DAYS
        )
        kwargs["refresh_token_expired_at"] = timezone.now() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRED_DAYS,
            hours=settings.REFRESH_TOKEN_EXPIRED_HOURS,
        )

        return self.create(**kwargs)

    def active_access_token(self):
        return self.filter(revoked_access_token=False)

    def not_expired_token(self):
        return self.filter(access_token_expired_at__gte=timezone.now())

    def valid_access_token(self):
        return self.active_access_token().not_expired_token()


class AccessToken(models.Model):
    access_token = models.CharField(max_length=255, unique=True)
    access_token_expired_at = models.DateTimeField()
    revoked_access_token = models.BooleanField(max_length=1, default=False)
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    refresh_token = models.CharField(max_length=255, unique=True)
    refresh_token_expired_at = models.DateTimeField()
    revoked_refresh_token = models.BooleanField(max_length=1, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccessTokenQuerySet.as_manager()

    def __str__(self):
        return self.access_token

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "access_token",
                    "revoked_access_token",
                    "access_token_expired_at",
                ]
            )
        ]


class VerificationQuerySet(models.query.QuerySet):
    def create_verification(self, *args, **kwargs):
        kwargs["expired_at"] = timezone.now() + timedelta(
            minutes=settings.VERIFICATION_EXPIRED_MINUTES
        )

        return self.create(**kwargs)

    def active(self):
        return self.filter(revoked=False)

    def not_expired(self):
        return self.filter(expired_at__gte=timezone.now())

    def valid(self):
        return self.active().not_expired()


class Verification(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    otp_reference = models.CharField(max_length=255, null=True)
    user = models.ForeignKey("user.User", on_delete=models.DO_NOTHING)
    client = models.ForeignKey("oauth.Client", on_delete=models.DO_NOTHING)
    revoked = models.BooleanField(default=False)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VerificationQuerySet.as_manager()

    def __str__(self):
        return self.reference

    class Meta:
        indexes = [
            models.Index(fields=["reference", "revoked", "expired_at"]),
        ]
