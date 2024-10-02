from django.shortcuts import render, get_object_or_404
from dj_rest_auth.registration.views import RegisterView
from signup.serializers import CustomRegisterSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Jersey
from .serializers import JerseySerializer
from rest_framework import status

# Home view
def home(request):
    return HttpResponse("Welcome to the homepage!")

# Custom user registration view
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class JerseyListView(APIView):
    def get(self, request):
        jerseys = Jersey.objects.prefetch_related('images').all()  # Prefetch images for efficiency
        serializer = JerseySerializer(jerseys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Jersey detail view (GET a single jersey by ID)
class JerseyDetailView(APIView):
    def get(self, request, id):
        jersey = get_object_or_404(Jersey, id=id)
        serializer = JerseySerializer(jersey)
        return Response(serializer.data)
