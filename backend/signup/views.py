from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from core.models import CustomUser

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
