from django.db import models
from django.conf import settings
from destinations.models import Destination

class Trip(models.Model):
    """
    Database model representing a traveler's planned trip.
    """
    TRAVEL_TYPE_CHOICES = [
        ('Solo', 'Solo'),
        ('Couple', 'Couple'),
        ('Family', 'Family'),
        ('Friends', 'Friends'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_travelers = models.PositiveIntegerField(default=1)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    travel_type = models.CharField(max_length=50, choices=TRAVEL_TYPE_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s trip to {self.destination.destination_name}"


class ItineraryTemplate(models.Model):
    """
    Database model representing predefined day-by-day travel plan templates.
    """
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='itinerary_templates'
    )
    day_number = models.PositiveIntegerField()
    morning = models.TextField()
    afternoon = models.TextField()
    evening = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['destination', 'day_number'], name='unique_destination_day')
        ]
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number} template for {self.destination.destination_name}"


class ItineraryDay(models.Model):
    """
    Database model representing actual traveler day-by-day trip itinerary details.
    """
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='itinerary_days'
    )
    day_number = models.PositiveIntegerField()
    morning = models.TextField()
    afternoon = models.TextField()
    evening = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip', 'day_number'], name='unique_trip_day')
        ]
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number} of {self.trip.user.username}'s trip to {self.trip.destination.destination_name}"
