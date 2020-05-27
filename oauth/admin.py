from django.contrib import admin
from oauth.models import Client, IPAddress, Grant, AccessToken


# Register your models here.
admin.site.register(Client)
admin.site.register(IPAddress)
admin.site.register(Grant)
admin.site.register(AccessToken)
