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


CustomUser = get_user_model()

# Logger setup
logger = logging.getLogger(__name__)

# Home view
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
        serializer = JerseySerializer(jersey, data=request.data, partial=True)  # Allow partial updates

        if serializer.is_valid():
            updated_jersey = serializer.save()

            # Log price history if the price has changed
            if updated_jersey.price != old_price:
                PriceHistory.objects.create(jersey=updated_jersey, price=updated_jersey.price)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            user = serializer.save(request)  # Pass the request here
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)

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

        refresh = RefreshToken.for_user(user)
        response = JsonResponse({'access': str(refresh.access_token), 'refresh': str(refresh)})
        response.set_cookie(key='refresh', value=str(refresh), httponly=True, samesite='Lax', secure=False)  # Adjust `secure` in production
        return response


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            else:
                # If no refresh token provided, just log the user out
                pass

            response = Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh')  # Clear refresh token cookie if it exists
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
        serializer.save(user=self.request.user)
        

class PriceAlertView(APIView):
    def post(self, request):
        jersey_id = request.data.get('jersey_id')
        email = request.user.email
        Alert.objects.create(user=request.user, jersey_id=jersey_id)

        return Response({"detail": "Price alert set."}, status=status.HTTP_201_CREATED)