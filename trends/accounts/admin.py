from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    class Meta:
        model = User

    list_display = ('usertype', 'email',)
    search_fields = ['email']
    list_filter = ('usertype',)
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2'), }),
        ("User Type", {'classes': ('wide',), 'fields': ('usertype',), }),
    )
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return super().get_fieldsets(request, obj)

        if obj.is_superuser:
            return (
                (None, {'fields': ('email', 'password', 'usertype',)}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            )
        else:
            return (
                (None, {'fields': ('email', 'password', 'usertype')}),
                ('Permissions', {'fields': ('is_active',)}),
            )


admin.site.register(User, UserAdmin)
