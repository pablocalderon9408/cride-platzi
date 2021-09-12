"""Users app."""

#Django
from django.apps import AppConfig

class UsersAppConfig(AppConfig):
    """Users app config    
    Important: every app must be installed in config - settings - base.py"""

    name = 'cride.users'
    verbose_name = 'Users'