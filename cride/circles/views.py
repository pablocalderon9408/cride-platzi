"""Circle views."""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from cride.circles.models import Circle

from cride.circles.serializers import (
    CreateCircleSerializer,
    CircleSerializer) 

@api_view(['GET'])
def list_circles(request):
    circles = Circle.objects.filter(is_public = True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_circle(request):
    """Create circle."""    
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)

# @api_view(['POST'])
# def create_circle(request):
#     """Create circle."""    
#     name = request.data['name']
#     slug_name = request.data['slug_name']
#     #Al parecer, al ponerlo de esta forma lo que hago 
#     # es poner el campo como opcional
#     about = request.data.get('about', '')
#     circle = Circle.objects.create(
#         name=name,
#         slug_name=slug_name, 
#         about=about)
#     data = {
#             'name': circle.name,
#             'slug_name': circle.slug_name,
#             'rides_taken': circle.rides_taken,
#             'rides_offered': circle.rides_offered,
#             'members_limit': circle.members_limit,        
#     }

#     return Response(data)