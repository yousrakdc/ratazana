from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Jersey
from .serializers import JerseySerializer
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator

# Home view
def home(request):
    return HttpResponse("Welcome to the homepage!")

# Jersey list view (GET all jerseys)
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

@ensure_csrf_cookie
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CheckLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Checking login for user:", request.user)
        if request.user.is_authenticated:
            print("User is authenticated")
        else:
            print("User is NOT authenticated")
        return JsonResponse({'isLoggedIn': request.user.is_authenticated})
