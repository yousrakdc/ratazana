from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings 


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    groups = models.ManyToManyField(
        Group,
        related_name='core_user_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='core_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='core_user_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='core_user'
    )

class Jersey(models.Model):
    brand = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='N/A') 
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(default='No description')
    season = models.CharField(max_length=10, default='N/A')
    sizes = models.TextField(default='N/A')        
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

