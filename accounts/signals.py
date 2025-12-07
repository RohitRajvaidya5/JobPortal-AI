from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import CandidateProfile, RecruiterProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    # Skip superuser
    if instance.is_superuser or instance.is_staff:
        return

    # Create recruiter profile
    try:
        if instance.role == User.RECRUITER:
            RecruiterProfile.objects.create(user=instance)

        # Create candidate profile
        elif instance.role == User.CANDIDATE:
            CandidateProfile.objects.create(user=instance)
    except AttributeError:
        # In case role or class constants aren't present, skip silently
        # (prevents errors during migrations or when using a different user model)
        return

