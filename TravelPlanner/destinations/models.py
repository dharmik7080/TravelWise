from django.db import models

class Destination(models.Model):
    """
    Database model representing a travel destination along with its geographical,
    economical, suitability, and rating metadata.
    """
    BUDGET_CHOICES = [
        ('Budget', 'Budget'),
        ('Moderate', 'Moderate'),
        ('Luxury', 'Luxury'),
    ]

    destination_id = models.AutoField(primary_key=True)
    destination_name = models.CharField(max_length=200, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100)
    description = models.TextField()
    best_season = models.CharField(max_length=100)
    ideal_days = models.PositiveIntegerField(default=1)
    budget_level = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    average_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    family_friendly = models.BooleanField(default=True)
    couple_friendly = models.BooleanField(default=True)
    solo_friendly = models.BooleanField(default=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)

    def __str__(self):
        return f"{self.destination_name} ({self.city})"
