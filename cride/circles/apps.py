"""Circles app."""

#Django
from django.apps import AppConfig

class CirclesAppConfig(AppConfig):
    """Circles app config    
    Important: every app must be installed in config - settings - base.py"""

    name = 'cride.circles'
    verbose_name = 'Circles'