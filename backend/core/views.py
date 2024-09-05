from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from signup.serializers import CustomRegisterSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
