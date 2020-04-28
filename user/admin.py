from django.contrib import admin
from .models import User, LoginEvent, Device


# Register your models here.
admin.site.register(User)
admin.site.register(LoginEvent)
admin.site.register(Device)
