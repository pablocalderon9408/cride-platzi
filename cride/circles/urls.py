
#Django
from django.urls import path

from cride.circles.models import Circle
from cride.circles.views import list_circles

urlpatterns = [
    path('circles/', list_circles)
    
]