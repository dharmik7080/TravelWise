from django.db import models
from destinations.models import Destination

class Package(models.Model):
    """
    Database model representing a travel package associated with a destination.
    """
    package_name = models.CharField(max_length=200, unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    duration = models.PositiveIntegerField(help_text="Duration of package in days", default=1)
    package_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='packages/', blank=True, null=True)

    def __str__(self):
        return f"{self.package_name} ({self.duration} Days)"
