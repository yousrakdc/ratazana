from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, JerseyListView, JerseyDetailView, csrf_token_view, CheckLoginView

urlpatterns = [
    path('', home, name='home'),
    path('api/jerseys/', JerseyListView.as_view(), name='jersey-list'),
    path('api/jerseys/<int:id>/', JerseyDetailView.as_view(), name='jersey-detail'),
    path('api/csrf-token/', csrf_token_view, name='csrf_token'),
    path('auth/check-login/', CheckLoginView.as_view(), name='check_login'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)