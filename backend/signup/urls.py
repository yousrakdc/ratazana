from django.urls import path, include
from .views import CustomRegisterView, LoginView, LogoutView, CheckLoginView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import csrf_token_view 

urlpatterns = [
    # Custom authentication routes
    path('signup/', CustomRegisterView.as_view(), name='custom_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # JWT Token management
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/csrf-token/', csrf_token_view, name='csrf_token'), 
    path('check-login/', CheckLoginView.as_view(), name='check_login'),
]
