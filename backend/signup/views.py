from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from core.models import CustomUser
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout

class CustomRegisterView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Incoming request data:", request.data)
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return JsonResponse({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'detail': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return JsonResponse({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({'detail': 'Login successful'})
            response.set_cookie(key='refresh', value=str(refresh), httponly=True, secure=False, samesite='Lax')
            response.set_cookie(key='access', value=str(refresh.access_token), httponly=True, secure=True, samesite='Lax')
            return response
        except Exception as e:
            print(f"Token generation failed: {e}")
            return JsonResponse({'detail': 'Token generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CheckLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Checking login for user:", request.user)
        return JsonResponse({'isLoggedIn': request.user.is_authenticated})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f'User authenticated: {request.user.is_authenticated}')
        if not request.user.is_authenticated:
            return Response({"detail": "Not authenticated."}, status=status.HTTP_403_FORBIDDEN)
        
        response = Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
