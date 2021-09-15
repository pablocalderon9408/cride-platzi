
#Django
from django.urls import path

from cride.circles.models import Circle
from cride.circles.views import create_circle,list_circles

urlpatterns = [
    path('circles/', list_circles),
    path('circles/create/', create_circle),
    
]