from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended profile for each user, holding avatar and saved destinations wishlist.
    Auto-created on User creation via post_save signal.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    saved_destinations = models.ManyToManyField(
        'destinations.Destination',
        blank=True,
        related_name='wishlisted_by'
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Auto-create or save profile whenever a User object is saved."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
