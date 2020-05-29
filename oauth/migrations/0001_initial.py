# Generated by Django 2.2.12 on 2020-05-27 14:07

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255, unique=True)),
                ('access_token_expired_at', models.DateTimeField(default=datetime.datetime(2020, 5, 28, 14, 7, 48, 371023, tzinfo=utc))),
                ('revoked_access_token', models.BooleanField(default=False, max_length=1)),
                ('refresh_token', models.CharField(max_length=255, unique=True)),
                ('refresh_token_expired_at', models.DateTimeField(default=datetime.datetime(2020, 5, 29, 2, 7, 48, 371115, tzinfo=utc))),
                ('revoked_refresh_token', models.BooleanField(default=False, max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('client_key', models.CharField(max_length=255, unique=True)),
                ('secret_key', models.CharField(max_length=255, unique=True)),
                ('revoked', models.BooleanField(default=False, max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('revoked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expired_at', models.DateTimeField(default=datetime.datetime(2020, 5, 27, 14, 12, 48, 370474, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=50)),
                ('revoked', models.BooleanField(default=False, max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255, unique=True)),
                ('otp_reference', models.CharField(max_length=255, null=True)),
                ('revoked', models.BooleanField(default=False)),
                ('expired_at', models.DateTimeField(default=datetime.datetime(2020, 5, 27, 14, 14, 48, 371794, tzinfo=utc))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='oauth.Client')),
            ],
        ),
    ]
