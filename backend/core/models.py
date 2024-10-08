from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email, username and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Normalize email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email, username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(Group, related_name='core_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='core_user_set', blank=True)

    def __str__(self):
        return self.email

class Jersey(models.Model):
    brand = models.CharField(max_length=500)
    team = models.CharField(max_length=500)
    country = models.CharField(max_length=500, default='N/A') 
    color = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # New field for original price
    description = models.TextField(default='No description')
    season = models.CharField(max_length=10, default='N/A')
    sizes = models.CharField(max_length=255, default='N/A') 
    image_path = models.ImageField(upload_to='jerseys/')  # This can be a single image if needed
    is_promoted = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=False)
    is_new_release = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} - {self.team}"

class JerseyImage(models.Model):
    jersey = models.ForeignKey(Jersey, related_name='images', on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='jerseys/')

    def __str__(self):
        return f"{self.jersey.team} Image"
    
class PriceHistory(models.Model):
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.jersey} - {self.price} on {self.date}"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.jersey}"

class Alert(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Alert for {self.user} on {self.jersey} ({self.alert_type})"

