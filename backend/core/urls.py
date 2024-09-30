from django.urls import path
from .views import home, jersey_list

urlpatterns = [
    path('', home, name='home'),
    path('api/jerseys/', jersey_list, name='jersey_list'),
]