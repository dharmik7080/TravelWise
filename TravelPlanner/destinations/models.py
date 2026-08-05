from django.db import models
from django.conf import settings

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

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.average_rating is not None and (self.average_rating < 0.0 or self.average_rating > 5.0):
            raise ValidationError({'average_rating': 'Rating must be between 0.0 and 5.0.'})
        if self.average_cost_per_day is not None and self.average_cost_per_day < 0:
            raise ValidationError({'average_cost_per_day': 'Average cost per day must be positive.'})
        if self.ideal_days is not None and self.ideal_days <= 0:
            raise ValidationError({'ideal_days': 'Ideal days must be greater than zero.'})

    def __str__(self):
        return f"{self.destination_name} ({self.city})"


class AIRecommendation(models.Model):
    """
    Model storing recommendation form parameters and scoring outcomes
    for logged-in and anonymous users.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Inputs
    budget = models.CharField(max_length=20)
    season = models.CharField(max_length=50)
    travel_type = models.CharField(max_length=20)
    duration = models.PositiveIntegerField()
    num_travellers = models.PositiveIntegerField()
    state = models.CharField(max_length=100, blank=True)
    
    # Outputs
    # Stores list of dicts: [{'destination_id': X, 'score': Y}, ...]
    results = models.JSONField(default=list)

    def __str__(self):
        return f"Recommendation for {self.user or 'Anonymous'} at {self.created_at}"

