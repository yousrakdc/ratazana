from django.urls import path
from .views import PromotedJerseysView

urlpatterns = [
    path('api/jerseys/promoted/', PromotedJerseysView.as_view(), name='promoted-jerseys'),
]