from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

CustomUser = get_user_model()

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
        """
        Check that the two password entries match.
        """
        if data.get('password1') != data.get('password2'):
            raise ValidationError(_("The two password fields must match."))
        return data

    def save(self, request):
        user = super().save(request)
        user.email = self.validated_data.get('email')
        user.username = self.validated_data.get('username')
        user.save()
        return user
