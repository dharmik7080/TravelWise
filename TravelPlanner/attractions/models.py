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

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.entry_fee is not None and self.entry_fee < 0:
            raise ValidationError({'entry_fee': 'Entry fee must be positive.'})
        if self.average_visit_time is not None and self.average_visit_time <= 0:
            raise ValidationError({'average_visit_time': 'Average visit time must be greater than zero.'})
        if self.opening_time and self.closing_time and self.opening_time >= self.closing_time:
            raise ValidationError('Opening time must be before closing time.')

    def __str__(self):
        return f"{self.attraction_name} - {self.destination.destination_name}"
