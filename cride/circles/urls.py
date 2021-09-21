
#Django
from django.urls import include, path
from rest_framework import urlpatterns

# from cride.circles.models import Circle
# from cride.circles.views import create_circle,list_circles

# urlpatterns = [
#     path('circles/', list_circles),
#     path('circles/create/', create_circle),
    
# ]


# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views

from cride.circles.views import circles as circle_views

router = DefaultRouter()

router.register(r'circles', circle_views.CircleViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls))
]

