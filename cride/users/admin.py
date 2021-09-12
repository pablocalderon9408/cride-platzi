
#Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cride.users.models import User, Profile


class CustomUserAdmin(UserAdmin):

    list_display=('email','username', 'first_name','last_name','is_client','is_staff')
    list_filter = ('is_client', 'is_staff', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display=('reputation','rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)


# User admin is registered this way as it is by default part of the admin.
admin.site.register(User, CustomUserAdmin)