from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'fullname', 'usertype', 'email', 'is_active')
    search_fields = ('username',)
    fieldsets = (
        ('Required Information', {'fields': ('username', 'password', 'usertype', 'last_login')}),
        ('Personal Information', {'fields': ('fullname', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('last_login',)


admin.site.register(User, UserAdmin)
