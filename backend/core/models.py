from django.db import models
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import logging
from django.core.mail import send_mail


logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')

        username = self.normalize_username(username) 
        user = self.model(username=username, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = [] 

    groups = models.ManyToManyField(Group, related_name='core_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='core_user_set', blank=True)

    def __str__(self):
        return self.username


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
        """Custom validation for the original_url field and sizes"""
        url_validator = URLValidator()

        # Validate original_url
        if self.original_url:
            try:
                url_validator(self.original_url)
            except ValidationError:
                self.original_url = None 

        # Validate sizes field (must be a list)
        if not isinstance(self.sizes, list):
            if isinstance(self.sizes, str):
                self.sizes = self.sizes.split('/')
            else:
                raise ValidationError("Sizes must be a list or a valid JSON array.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Jersey, self).save(*args, **kwargs)
        
    def get_current_price(self):
        logger.info(f"Current price for jersey {self.id}: {self.price}")
        return self.price 

    def update_price(self, new_price):
        logger.info(f"Updating price for jersey {self.id}: from {self.price} to {new_price}")
        self.last_known_price = self.price 
        self.price = new_price               
        self.save()                          



    def notify_price_drop(self, new_price):
        alerts = Alert.objects.filter(jersey=self, status='active', alert_type='price_drop')
        for alert in alerts:
            alert.trigger_alert()
            print(f"Triggered price drop alert for Jersey ID {self.id} and Alert ID {alert.id}.")


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
        ('viewed', 'Viewed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.alert_type} alert for {self.user} on {self.jersey} (Status: {self.status})"

    def trigger_alert(self):
        self.status = 'triggered'
        send_email_notification(self.user.email, self.jersey) 
        self.save()

def send_email_notification(email, jersey):
    logger = logging.getLogger(__name__)

    subject = 'Price Alert Triggered!'
    message = (
        f'The price for {jersey.brand} {jersey.team} jersey has changed. '
        f'The new price is {jersey.price}.'
    )
    
    try:
        send_mail(subject, message, 'from@example.com', [email])
        logger.info(f'Email sent to {email} for jersey {jersey.id} with new price {jersey.price}.')
    except Exception as e:
        logger.error(f'Error sending email to {email}: {str(e)}')
