# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
ENUM_CHOICE = (
    ('Y', 'Yes'),
    ('N', 'No')
)


class Client(models.Model):
    client_name = models.CharField(max_length=50)
    client_public_key = models.CharField(max_length=100, unique=True)
    client_secret_key = models.CharField(max_length=100, unique=True)
    callback_url = models.CharField(max_length=255, unique=True)
    is_enabled = models.CharField(max_length=1, choices=ENUM_CHOICE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.client_name


class AccessToken(models.Model):
    access_token = models.CharField(max_length=150, unique=True)
    user = models.ForeignKey('users.User', db_column='user_id')
    client = models.ForeignKey('oauth.Client', db_column='client_id')
    refresh_token = models.CharField(max_length=150, unique=True)
    expired_at = models.DateTimeField(null=True)
    is_refresh_token_used = models.CharField(max_length=1, choices=ENUM_CHOICE, default='N')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.access_token


class Grant(models.Model):
    grant_code = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey('oauth.Client', null=True, db_column='client_id')
    user = models.ForeignKey('users.User', null=True, db_column='user_id')
    ip_address = models.CharField(max_length=50)
    revoked = models.SmallIntegerField(db_column='revoked', default=False)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.grant_code
