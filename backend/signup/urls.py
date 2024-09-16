from django.urls import path
from .views import CustomRegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='custom_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
