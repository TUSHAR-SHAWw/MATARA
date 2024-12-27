
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """
    Create or save the UserProfile when a User is created or saved.
    """
    if created:
        # Create a new UserProfile for the new User
        UserProfile.objects.create(user=instance)
    else:
        # Save the UserProfile if it already exists
        if not hasattr(instance, 'profile'):
            # If no profile exists, create one
            UserProfile.objects.create(user=instance)
        else:
            # Otherwise, just save the existing profile
            instance.profile.save()