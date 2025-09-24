from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserPreference


@receiver(post_save, sender=User)
def create_user_preference(sender, instance, created, **kwargs):
    if created:
        # Automatically create a UserPreference for every new user
        UserPreference.objects.create(owner=instance, currency='USD')
