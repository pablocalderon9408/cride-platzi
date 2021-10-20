
#Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#Models
from cride.users.models import User, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display=('user','reputation','rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)
    fieldsets = (
    ('Profile', {
      'fields': (
        ('user', 'picture'),
        ('biography')
      )
    }),
    ('Stats', {
      'fields': (
        ('reputation'),
        ('rides_taken', 'rides_offered'),
      )
    }),
    ('Metadata', {
      'fields': (('created', 'modified'),),
    })
  )

    readonly_fields = ('created', 'modified')

class ProfileInLine(admin.StackedInline):
  model = Profile
  can_delete = False
  verbose_name_plural = 'profiles'


class CustomUserAdmin(UserAdmin):

    """User model admin"""

    inlines = (ProfileInLine,)
    list_display=('email','username', 'first_name','last_name','is_client','is_staff')
    list_filter = ('is_client', 'is_staff', 'created', 'modified')

# User admin is registered this way as it is by default part of the admin.
admin.site.register(User, CustomUserAdmin)