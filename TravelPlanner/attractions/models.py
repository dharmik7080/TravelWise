from django.db import models
from destinations.models import Destination

class Attraction(models.Model):
    """
    Database model representing a tourist attraction located at a specific destination.
    """
    attraction_name = models.CharField(max_length=200, unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    category = models.CharField(max_length=100)
    description = models.TextField()
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    average_visit_time = models.PositiveIntegerField(help_text="Average visit time in minutes", default=60)
    image = models.ImageField(upload_to='attractions/', blank=True, null=True)

    def __str__(self):
        return f"{self.attraction_name} - {self.destination.destination_name}"
