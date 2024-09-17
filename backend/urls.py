from django.contrib import admin
from django.urls import path, include
from core.views import home


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('signup.urls')),  # This includes login at /auth/login/
    path('', include('jerseys.urls')), 
]
