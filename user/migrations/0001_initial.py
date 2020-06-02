# Generated by Django 2.2.12 on 2020-06-02 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=255, unique=True)),
                ('ip_address', models.CharField(max_length=50)),
                ('platform', models.CharField(max_length=255, null=True)),
                ('platform_version', models.CharField(max_length=50, null=True)),
                ('browser', models.CharField(max_length=255, null=True)),
                ('browser_version', models.CharField(max_length=50, null=True)),
                ('device', models.CharField(max_length=255, null=True)),
                ('device_version', models.CharField(max_length=50, null=True)),
                ('revoked', models.BooleanField(default=False, max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoginEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=50)),
                ('platform', models.CharField(max_length=255, null=True)),
                ('platform_version', models.CharField(max_length=50, null=True)),
                ('browser', models.CharField(max_length=255, null=True)),
                ('browser_version', models.CharField(max_length=50, null=True)),
                ('device', models.CharField(max_length=255, null=True)),
                ('device_version', models.CharField(max_length=50, null=True)),
                ('action', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255, null=True, unique=True)),
                ('confirmed_account', models.BooleanField(default=False)),
                ('revoked', models.BooleanField(default=False)),
                ('otp_email_enabled', models.BooleanField(default=False)),
                ('failed_login_attempt', models.SmallIntegerField(default=0)),
                ('pp_path', models.CharField(max_length=255, null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email', 'confirmed_account', 'revoked', 'failed_login_attempt'], name='user_user_email_e92655_idx'),
        ),
        migrations.AddField(
            model_name='loginevent',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='oauth.Client'),
        ),
        migrations.AddField(
            model_name='device',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='oauth.Client'),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.User'),
        ),
    ]
