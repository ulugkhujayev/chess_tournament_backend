from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    actions = ["make_admin", "remove_admin"]

    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)

    make_admin.short_description = "Mark selected users as admins"

    def remove_admin(self, request, queryset):
        queryset.update(is_admin=False)

    remove_admin.short_description = "Remove admin status from selected users"


admin.site.register(User, CustomUserAdmin)
