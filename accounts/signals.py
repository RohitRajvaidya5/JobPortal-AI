from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CandidateProfile, RecruiterProfile

User = settings.AUTH_USER_MODEL

from django.apps import apps

@receiver(post_save)
def create_user_profile(sender, instance, created, **kwargs):
    # Only run for your custom User class
    UserModel = apps.get_model(settings.AUTH_USER_MODEL)
    if sender is not UserModel:
        return
    if created:
        if instance.role == UserModel.CANDIDATE:
            CandidateProfile.objects.create(user=instance)
        elif instance.role == UserModel.RECRUITER:
            RecruiterProfile.objects.create(user=instance)
        # Admin role can be handled by is_staff / is_superuser
