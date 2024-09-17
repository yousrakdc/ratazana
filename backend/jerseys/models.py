from django.db import models

class Jersey(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    team = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    season = models.DecimalField(max_digits=8, decimal_places=0)
    is_promoted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    