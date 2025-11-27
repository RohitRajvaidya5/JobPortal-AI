from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CandidateProfile, RecruiterProfile

User = settings.AUTH_USER_MODEL

from django.apps import apps

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    # Skip superuser
    if instance.is_superuser or instance.is_staff:
        return

    # Create recruiter profile
    if instance.role == User.RECRUITER:
        RecruiterProfile.objects.create(user=instance)

    # Create candidate profile
    elif instance.role == User.CANDIDATE:
        CandidateProfile.objects.create(user=instance)

