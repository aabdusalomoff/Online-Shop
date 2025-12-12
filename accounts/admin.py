from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseAdminUser

from .models import User

@admin.register(User)
class UserAdmin(BaseAdminUser):
    list_display = ['username','phone','email','is_active']
    list_filter = ['is_active','is_superuser','date_joined','is_staff']