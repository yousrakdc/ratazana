from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from signup.serializers import CustomRegisterSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the homepage!")

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
