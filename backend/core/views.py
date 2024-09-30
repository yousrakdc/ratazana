from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from signup.serializers import CustomRegisterSerializer
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Jersey
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .serializers import JerseySerializer
from rest_framework.exceptions import NotFound

def home(request):
    return HttpResponse("Welcome to the homepage!")

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

@api_view(['GET'])
def jersey_list(request):
    try:
        jerseys = Jersey.objects.all()
        serializer = JerseySerializer(jerseys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error fetching jerseys:", str(e))
        return Response({'error': 'An error occurred while fetching jerseys.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)