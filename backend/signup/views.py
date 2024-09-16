# backend/signup/views.py
from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from core.models import CustomUser
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check for missing fields
        if not email or not password:
            return JsonResponse({'detail': 'Email and password are required'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'detail': 'Invalid email format'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'detail': 'Invalid credentials'}, status=401)

        if not user.check_password(password):
            return JsonResponse({'detail': 'Invalid credentials'}, status=401)

        email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()
        if not email_verified:
            return JsonResponse({'detail': 'Email is not verified'}, status=400)

        try:
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({'detail': 'Login successful'})
            
            # Set JWT tokens as HttpOnly cookies
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            
            return response
        except Exception as e:
            return JsonResponse({'detail': 'Token generation failed'}, status=500)
