from django.db import models

# Create your models here.
from django.db import models

class Court(models.Model):
    SPORT_CHOICES = [
        ('badminton', 'Badminton'),
        ('tennis', 'Tennis'),
        ('pickleball', 'Pickleball'),
    ]

    name = models.CharField(max_length=100)
    sport_type = models.CharField(max_length=20, choices=SPORT_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.sport_type})"

