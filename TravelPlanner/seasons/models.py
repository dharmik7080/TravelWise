from django.db import models
from destinations.models import Destination

class BestSeason(models.Model):
    """
    Database model representing weather patterns and seasonal parameters for a destination.
    """
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='best_seasons')
    season = models.CharField(max_length=100)
    peak_months = models.CharField(max_length=200)
    average_temperature = models.CharField(max_length=100)
    rainfall = models.CharField(max_length=100)
    travel_tip = models.TextField()

    def __str__(self):
        return f"{self.season} at {self.destination.destination_name}"
