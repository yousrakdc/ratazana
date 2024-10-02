from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, JerseyListView, JerseyDetailView

urlpatterns = [
    path('', home, name='home'),
    path('api/jerseys/', JerseyListView.as_view(), name='jersey-list'),
    path('jerseys/<int:id>/', JerseyDetailView.as_view(), name='jersey-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)