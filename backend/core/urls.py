from django.urls import path, include
from rest_framework.routers import DefaultRouter
from views import JerseyViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'jerseys', JerseyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)