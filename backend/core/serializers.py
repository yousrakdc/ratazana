from rest_framework import serializers
from .models import Jersey, JerseyImage

class JerseyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JerseyImage
        fields = ['image_path']

class JerseySerializer(serializers.ModelSerializer):
    images = JerseyImageSerializer(many=True, read_only=True)  # Ensure this is set up

    class Meta:
        model = Jersey
        fields = [
            'id', 
            'brand', 
            'team', 
            'country', 
            'color', 
            'price', 
            'description', 
            'season', 
            'is_promoted', 
            'is_upcoming', 
            'is_new_release',
            'images',  # Include images field
        ]
