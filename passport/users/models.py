from django.db import models


# Create your models here.
ENUM_CHOICE = (
    (1, 'Yes'),
    (0, 'No')
)
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=70, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, null=True)
    confirmation_code = models.CharField(max_length=150, unique=True, null=True)
    confirmed_account = models.BooleanField(max_length=1, choices=ENUM_CHOICE, default=False)
    is_admin = models.BooleanField(max_length=1, choices=ENUM_CHOICE, default=False)
    path = models.CharField(max_length=50, null=True)
    profile_picture = models.CharField(max_length=100, null=True)
    last_login = models.DateTimeField(null=True)
    last_login_ip_address = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name