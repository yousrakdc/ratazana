from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='core_user_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='core_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='core_user_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='core_user'
    )

class Jersey(models.Model):
    brand = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.brand} - {self.team}"

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
