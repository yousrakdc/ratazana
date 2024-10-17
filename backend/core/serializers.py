from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Jersey, JerseyImage, Like, PriceHistory, Alert

CustomUser = get_user_model()

# Serializer for Jersey Images
class JerseyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JerseyImage
        fields = ['image_path']

# Serializer for Jerseys
class JerseySerializer(serializers.ModelSerializer):
    images = JerseyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Jersey
        fields = [
            'id', 
            'brand', 
            'team', 
            'country', 
            'color', 
            'price',
            'sizes', 
            'description', 
            'season',
            'original_url',
            'is_promoted', 
            'is_upcoming', 
            'is_new_release',
            'images',
        ]

    def update(self, instance, validated_data):
        # Store the old price before updating
        old_price = instance.price
        
        # Update the instance
        instance = super().update(instance, validated_data)

        # Create a price history entry only if the price has changed
        new_price = validated_data.get('price', old_price)
        if new_price != old_price:
            PriceHistory.objects.create(jersey=instance, price=new_price)

        return instance

# Serializer for Likes
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'jersey']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# Custom User Registration Serializer
class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(_("Username already taken. Be more creative."))
        return username

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_('Email already registered.'))
        return email

    def validate_password1(self, password):
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        return password

    def validate(self, data):
        if data.get('password1') != data.get('password2'):
            raise ValidationError(_("The two password fields must match."))
        return data

    def save(self, request):
        user = super().save(request)
        user.email = self.validated_data.get('email')
        user.username = self.validated_data.get('username')
        user.save()
        return user
    
class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'jersey', 'price', 'date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.isoformat()
        return representation
    
class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'user', 'jersey', 'target_price', 'created_at']
        read_only_fields = ['user', 'created_at']