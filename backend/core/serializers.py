from rest_framework import serializers
from .models import Jersey

class JerseySerializer(serializers.ModelSerializer):
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
            'image_path', 
            'is_promoted', 
            'is_upcoming', 
            'is_new_release'
        ]

        
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
