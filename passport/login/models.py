from django.db import models
import datetime

# Create your models here.
ENUM_CHOICE = (
    ('Y', 'Yes'),
    ('N', 'No')
)
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=70, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, null=True)
    confirmation_code = models.CharField(max_length=150, unique=True, null=True)
    confirmed_account = models.CharField(max_length=1, choices=ENUM_CHOICE, default='N')
    is_admin = models.CharField(max_length=1, choices=ENUM_CHOICE, default='N')
    path = models.CharField(max_length=50, null=True)
    profile_picture = models.CharField(max_length=100, null=True)
    last_login = models.DateTimeField(null=True)
    last_login_ip_address = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

class OauthClient(models.Model):
    client_name = models.CharField(max_length=50)
    client_public_key = models.CharField(max_length=100, unique=True)
    client_secret_key = models.CharField(max_length=100, unique=True)
    callback_url = models.CharField(max_length=255, unique=True)
    is_enabled = models.CharField(max_length=1, choices=ENUM_CHOICE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'oauth_clients'

    def __str__(self):
        return self.client_name

class OauthAccessToken(models.Model):
    access_token = models.CharField(max_length=150, unique=True)
    user = models.ForeignKey(User, db_column='user_id')
    client = models.ForeignKey(OauthClient, db_column='client_id')
    refresh_token = models.CharField(max_length=150, unique=True)
    expired_at = models.DateTimeField(null=True)
    is_refresh_token_used = models.CharField(max_length=1, choices=ENUM_CHOICE, default='N')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'oauth_access_token'

    def __str__(self):
        return self.access_token

class OauthGrant(models.Model):
    grant_code = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(OauthClient, null=True, db_column='client_id')
    user = models.ForeignKey(User, null=True, db_column='user_id')
    ip_address = models.CharField(max_length=50)
    revoked = models.SmallIntegerField(db_column='revoked', default=False)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'oauth_grants'

    def __str__(self):
        return self.grant_code
