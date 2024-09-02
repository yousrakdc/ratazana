from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Add additional fields if necessary

# Jersey Model
class Jersey(models.Model):
    brand = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # You can add more fields such as season, size, etc., as needed

    def __str__(self):
        return f"{self.brand} {self.team} Jersey"

# PriceHistory Model
class PriceHistory(models.Model):
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE, related_name='price_histories')
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Price on {self.date} for {self.jersey}"

# Like Model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE, related_name='liked_by')

    def __str__(self):
        return f"{self.user.username} likes {self.jersey}"

# Alert Model
class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    jersey = models.ForeignKey(Jersey, on_delete=models.CASCADE, related_name='alerts')
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Alert for {self.user.username} on {self.jersey} at {self.desired_price}"
