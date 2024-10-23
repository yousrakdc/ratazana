from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, 
    JerseyListView, 
    JerseyDetailView, 
    csrf_token_view, 
    CheckLoginView, 
    CustomRegisterView, 
    LoginView, 
    LogoutView, 
    LikeToggleView,
    LikedJerseysView,
    PriceHistoryView,
    PriceAlertView,
    UserAlertsView,           
    MarkAlertViewedView,
    start_oauth,
    oauth2callback,
    success_view,     
)

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Home view
    path('', home, name='home'),

    # Jersey API routes
    path('api/jerseys/', JerseyListView.as_view(), name='jersey-list'),
    path('api/jerseys/<int:id>/', JerseyDetailView.as_view(), name='jersey-detail'),

    # CSRF token route
    path('api/csrf-token/', csrf_token_view, name='csrf_token'),

    # Custom authentication routes
    path('auth/signup/', CustomRegisterView.as_view(), name='custom_signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # JWT Token management
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Check login status
    path('auth/check-login/', CheckLoginView.as_view(), name='check_login'),

    # Like routes
    path('api/jerseys/<int:jersey_id>/likes/', LikeToggleView.as_view(), name='like-toggle'),
    path('api/jerseys/likes/', LikedJerseysView.as_view(), name='liked_jerseys'),
    
    path('api/jerseys/<int:id>/price-history/', PriceHistoryView.as_view(), name='price-history'),
    path('price-alerts/', PriceAlertView.as_view(), name='price-alerts'),

    # Alert endpoints
    path('api/alerts/', UserAlertsView.as_view(), name='user-alerts'), 
    path('api/alerts/<int:alert_id>/viewed/', MarkAlertViewedView.as_view(), name='mark-alert-viewed'),
    
    # Oauth
    path('start_oauth/', start_oauth, name='start_oauth'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
    path('success/', success_view, name='success_url'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
