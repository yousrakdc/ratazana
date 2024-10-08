from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, csrf_token_view, CheckLoginView


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('dj_rest_auth.urls')),  # This includes login at /auth/login/
    path('auth/signup/', include('dj_rest_auth.registration.urls')),
    path('auth/api/csrf-token/', csrf_token_view, name='csrf_token'),
    path('auth/check-login/', CheckLoginView.as_view(), name='check_login'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)