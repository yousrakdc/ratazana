from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Jersey, Like, PriceHistory, Alert
from .serializers import JerseySerializer, CustomRegisterSerializer, LikeSerializer, PriceHistorySerializer, AlertSerializer
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.middleware.csrf import get_token
import logging
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.shortcuts import redirect
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import pickle
from django.http import HttpResponse
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import random 
import string 
from django.shortcuts import get_object_or_404



CustomUser = get_user_model()

logger = logging.getLogger(__name__)

def home(request):
    return JsonResponse({"message": "Welcome to the homepage!"})


class JerseyListView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        filter_kwargs = {}

        if category == 'promoted':
            filter_kwargs['is_promoted'] = True
        elif category == 'new_release':
            filter_kwargs['is_new_release'] = True
        elif category == 'upcoming':
            filter_kwargs['is_upcoming'] = True

        jerseys = Jersey.objects.prefetch_related('images').filter(**filter_kwargs) if filter_kwargs else Jersey.objects.prefetch_related('images').all()
        serializer = JerseySerializer(jerseys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JerseyDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        jersey = get_object_or_404(Jersey, id=id)
        serializer = JerseySerializer(jersey)
        return Response(serializer.data)

    def put(self, request, id):
        jersey = get_object_or_404(Jersey, id=id)
        old_price = jersey.price  # Store the old price before updating
        serializer = JerseySerializer(jersey, data=request.data, partial=True)

        if serializer.is_valid():
            updated_jersey = serializer.save()

            # Log price history if the price has changed
            if updated_jersey.price != old_price:
                PriceHistory.objects.create(jersey=updated_jersey, price=updated_jersey.price)
                # Check alerts after price change
                self.check_alerts(updated_jersey)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_alerts(self, jersey):
        alerts = Alert.objects.filter(jersey=jersey, status='active')
        for alert in alerts:
            alert.check_trigger()



@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'csrfToken': get_token(request)})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CheckLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        return JsonResponse({'isLoggedIn': request.user.is_authenticated})


class LikeToggleView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        jersey_id = self.kwargs.get('jersey_id')
        return Like.objects.filter(jersey_id=jersey_id)

    def perform_create(self, serializer):
        jersey_id = self.kwargs.get('jersey_id')
        if Like.objects.filter(jersey_id=jersey_id, user=self.request.user).exists():
            raise ValidationError("You have already liked this jersey.")
        serializer.save(user=self.request.user, jersey_id=jersey_id)

    def delete(self, request, *args, **kwargs):
        jersey_id = self.kwargs.get('jersey_id')
        try:
            like = Like.objects.get(jersey_id=jersey_id, user=self.request.user)
            like.delete()
            return Response({"detail": "Jersey unliked successfully."}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"detail": "You have not liked this jersey."}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        is_liked = queryset.filter(user=request.user).exists()
        return Response({'is_liked': is_liked})
    
class CustomRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save(request)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return JsonResponse({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
            user = CustomUser.objects.get(email=email)
        except (DjangoValidationError, CustomUser.DoesNotExist):
            return JsonResponse({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return JsonResponse({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # If everything is valid, generate tokens
        refresh = RefreshToken.for_user(user)
        response = JsonResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh)  
        })
        
        # Set the refresh token in a HttpOnly cookie
        response.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            samesite='Lax',
            secure=False  # Set to `True` if using HTTPS in production
        )

        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Validate the refresh token and blacklist it
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)

            response.delete_cookie('refresh')
            return response
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response({"detail": f"Logout failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class LikedJerseysView(generics.ListAPIView):
    serializer_class = JerseySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Jersey.objects.filter(likes__user=user)
    
    
class PriceHistoryView(generics.ListAPIView):
    serializer_class = PriceHistorySerializer

    def get_queryset(self):
        jersey_id = self.kwargs['id']
        try:
            jersey = Jersey.objects.get(id=jersey_id)
            return jersey.price_history.all().order_by('date')
        except Jersey.DoesNotExist:
            raise NotFound("Jersey not found")


class AlertCreateView(generics.CreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        target_price = self.request.data.get('target_price')
        alert_type = self.request.data.get('alert_type')
        
        if target_price is None or alert_type is None:
            raise ValidationError("target_price and alert_type are required.")
        
        serializer.save(user=self.request.user, target_price=target_price, alert_type=alert_type)


class PriceAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        jersey_id = request.data.get('jersey_id')
        
        if not jersey_id:
            return Response({"error": "jersey_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        Alert.objects.create(user=request.user, jersey_id=jersey_id, alert_type='price_drop')
        return Response({"detail": "Price alert set."}, status=status.HTTP_201_CREATED)
 
class UserAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        jersey_id = request.data.get('jersey_id')

        if jersey_id is None:
            return Response({"error": "jersey_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        Alert.objects.create(user=request.user, jersey_id=jersey_id, alert_type='price_drop')

        return Response({"detail": "Price alert set."}, status=status.HTTP_201_CREATED)

    def get(self, request):
        alerts = Alert.objects.filter(user=request.user, status='triggered')
        alert_data = [
            {"id": alert.id, "jersey": alert.jersey.brand, "alert_type": alert.alert_type, "created_at": alert.created_at}
            for alert in alerts
        ]
        return Response(alert_data)


class MarkAlertViewedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, alert_id):
        try:
            alert = Alert.objects.get(id=alert_id, user=request.user)
            alert.mark_as_viewed()
            return Response({"status": "success"}, status=200)
        except Alert.DoesNotExist:
            return Response({"error": "Alert not found."}, status=404)

class AlertView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alerts = Alert.objects.filter(status='active', user=request.user)
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)

    def post(self, request, alert_id):
        try:
            alert = Alert.objects.get(id=alert_id, user=request.user)
            if alert.status == 'viewed':
                return Response({"error": "Alert already viewed."}, status=status.HTTP_400_BAD_REQUEST)

            alert.status = 'viewed'
            alert.save()
            return Response({"status": "Alert marked as viewed."}, status=status.HTTP_200_OK)
        except Alert.DoesNotExist:
            return Response({"error": "Alert not found."}, status=status.HTTP_404_NOT_FOUND)


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

def start_oauth(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(BASE_DIR, 'backend', 'core', 'management', 'commands', 'credentials.json'),
        SCOPES
    )
    
    flow.redirect_uri = 'https://68ef-77-136-104-119.ngrok-free.app/oauth2callback/'

    # Generate the authorization URL with the correct scope
    authorization_url, state = flow.authorization_url(
        access_type='offline', 
        include_granted_scopes='true', 
    )

    # Store the state in the session for later validation
    request.session['state'] = state

    return redirect(authorization_url)

def oauth2callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if state != request.session.get('state'):
        return HttpResponse("Invalid state parameter.", status=403)

    if not code:
        return HttpResponse("No authorization code provided.", status=400)

    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(BASE_DIR, 'backend', 'core', 'management', 'commands', 'credentials.json'),
        SCOPES
    )
    
    flow.redirect_uri = 'https://68ef-77-136-104-119.ngrok-free.app/oauth2callback/'

    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials

        if not credentials.refresh_token:
            return HttpResponse("No refresh token returned. Ensure your scopes and access type are correct.", status=400)

        # Save the credentials to token.json
        token_path = os.path.join(BASE_DIR, 'backend', 'core', 'token.json')
        os.makedirs(os.path.dirname(token_path), exist_ok=True) 

        with open(token_path, 'w') as token_file:
            token_file.write(credentials.to_json())

        return redirect('success_url')
    except Exception as e:
        print(f"Error during token exchange: {str(e)}")
        return HttpResponse(f"Error exchanging token: {str(e)}", status=500)

def success_view(request):
    return HttpResponse("Authentication successful! You can now use the app.")