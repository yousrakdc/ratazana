from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """Create and return a user with a username and password."""
        if not username:
            raise ValueError('The username field must be set')
        
        username = self.normalize_username(username)  # Normalize username
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Create and return a superuser with a username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    
    USERNAME_FIELD = 'username'  # Set the USERNAME_FIELD to username
    REQUIRED_FIELDS = []  # No required fields, since username is used for authentication

    groups = models.ManyToManyField(Group, related_name='core_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='core_user_set', blank=True)

    def __str__(self):
        return self.username  # Return username instead of email


from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib.auth.models import User

class Jersey(models.Model):
    brand = models.CharField(max_length=500)
    team = models.CharField(max_length=500)
    country = models.CharField(max_length=500, default='N/A')
    color = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(default='No description')
    season = models.CharField(max_length=10, default='N/A')
    sizes = models.JSONField(default=list)
    original_url = models.URLField(max_length=500, blank=True, null=True)
    image_path = models.ImageField(upload_to='jerseys/')
    is_promoted = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=False)
    is_new_release = models.BooleanField(default=False)
    last_known_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True) 

    def clean(self):
        """ Custom validation for the original_url field and sizes """
        url_validator = URLValidator()

        # Validate original_url
        if self.original_url:
            try:
                url_validator(self.original_url)
            except ValidationError:
                self.original_url = None  # or raise ValidationError('Invalid URL')

        # Validate sizes field (must be a list)
        if not isinstance(self.sizes, list):
            if isinstance(self.sizes, str):
                # If it's a string, try to convert it to a list
                self.sizes = self.sizes.split('/')  # Assuming sizes like "S/M/L" format
            else:
                raise ValidationError("Sizes must be a list or a valid JSON array.")

    def save(self, *args, **kwargs):
        # Call the clean method before saving
        self.clean()
        super(Jersey, self).save(*args, **kwargs)

    def update_price(self, new_price):
        """ Update the price and check if it has dropped. """
        if new_price < self.last_known_price:
            self.notify_price_drop(new_price)  # Notify if price has dropped
        self.last_known_price = self.price  # Update last known price
        self.price = new_price  # Set the new price
        self.save()  # Save the model with updated values

    def notify_price_drop(self, new_price):
        """ Logic for notifying users about the price drop. """
        # Here you would include logic to notify users, e.g.:
        print(f"Price for {self.brand} {self.team} has dropped from {self.last_known_price} to {new_price}.")
        # You could integrate with your notification system or send emails here

    def __str__(self):
        return f"{self.brand} {self.team}"


class JerseyImage(models.Model):
    jersey = models.ForeignKey(Jersey, related_name='images', on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='jerseys/')

    def __str__(self):
        return f"{self.jersey.team} Image"
    
class PriceHistory(models.Model):
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, null=True) 

    class Meta:
        unique_together = ('user', 'jersey') 

    def __str__(self):
        return f"{self.user} likes {self.jersey}"


class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('price_drop', 'Price Drop'),
        ('price_increase', 'Price Increase'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('triggered', 'Triggered'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.alert_type} alert for {self.user} on {self.jersey} (Status: {self.status})"

    def check_trigger(self):
        """Check if the alert should be triggered based on the current price of the jersey."""
        current_price = self.jersey.price
        if self.alert_type == 'price_drop' and current_price < self.target_price:
            self.trigger_alert()
        elif self.alert_type == 'price_increase' and current_price > self.target_price:
            self.trigger_alert()

    def trigger_alert(self):
        """Trigger the alert and change the status."""
        # Implement notification logic here (e.g., send an email)
        self.status = 'triggered'
        self.save()
