from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Client

class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Client Info'

class UserAdmin(BaseUserAdmin):
    inlines = (ClientInline,)

# Unregister the original User admin
admin.site.unregister(User)
# Register the User admin with the Client inline
admin.site.register(User, UserAdmin)
