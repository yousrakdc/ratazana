from django.shortcuts import render, get_object_or_404
from dj_rest_auth.registration.views import RegisterView
from signup.serializers import CustomRegisterSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Jersey
from .serializers import JerseySerializer
from rest_framework import status

# Home view
def home(request):
    """Return a welcome message for the homepage."""
    return HttpResponse("Welcome to the homepage!")

# Custom user registration view
class CustomRegisterView(RegisterView):
    """Handle user registration with a custom serializer."""
    serializer_class = CustomRegisterSerializer

class JerseyListView(APIView):
    """View to list jerseys with optional filtering by category."""
    
    def get(self, request):
        """Handle GET request to retrieve jerseys."""
        # Get the category parameter from the request
        category = request.query_params.get('category')

        # Filter jerseys based on the category parameter
        if category == 'promoted':
            jerseys = Jersey.objects.filter(is_promoted=True).prefetch_related('images')
        elif category == 'upcoming':
            jerseys = Jersey.objects.filter(is_upcoming=True).prefetch_related('images')
        elif category == 'new_release':
            jerseys = Jersey.objects.filter(is_new_release=True).prefetch_related('images')
        else:
            jerseys = Jersey.objects.prefetch_related('images').all()  # Default: return all jerseys

        serializer = JerseySerializer(jerseys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JerseyDetailView(APIView):
    """View to retrieve details of a specific jersey by ID."""
    
    def get(self, request, id):
        """Handle GET request to retrieve a single jersey by ID."""
        jersey = get_object_or_404(Jersey, id=id)
        serializer = JerseySerializer(jersey)
        
        # Adding additional image details
        jersey_data = {
            "id": jersey.id,
            "brand": jersey.brand,
            "team": jersey.team,
            "country": jersey.country,
            "color": jersey.color,
            "price": str(jersey.price),
            "description": jersey.description,
            "season": jersey.season,
            "is_promoted": jersey.is_promoted,
            "is_upcoming": jersey.is_upcoming,
            "is_new_release": jersey.is_new_release,
            "images": [
                {
                    "id": image.id,
                    "image_path": image.image_path.url
                } for image in jersey.images.all()
            ]
        }
        
        return Response(jersey_data, status=status.HTTP_200_OK)