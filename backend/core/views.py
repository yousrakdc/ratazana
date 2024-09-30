from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from signup.serializers import CustomRegisterSerializer
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Jersey
from .serializers import JerseySerializer

def home(request):
    return HttpResponse("Welcome to the homepage!")

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class JerseyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Jersey.objects.all()
    serializer_class = JerseySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'promoted' in self.request.query_params:
            queryset = queryset.filter(is_promoted=True)
        if 'upcoming' in self.request.query_params:
            queryset = queryset.filter(is_upcoming=True)
        if 'new_release' in self.request.query_params:
            queryset = queryset.filter(is_new_release=True)
        return queryset
