from django.urls import path
from .views import CustomRegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='custom_signup'),
    path('login/', LoginView.as_view(), name='login'),  # Added login endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint
]
