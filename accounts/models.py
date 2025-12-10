from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# If using Django >= 3.1 and PostgreSQL (recommended), use JSONField:
try:
    # Django's built-in JSONField (works for Postgres and some DBs)
    from django.db.models import JSONField
except ImportError:
    JSONField = None  # fallback handled below


class User(AbstractUser):
    # Role choices
    CANDIDATE = 'candidate'
    RECRUITER = 'recruiter'
    ADMIN = 'admin'   # you can also rely on is_staff/is_superuser
    ROLE_CHOICES = [
        (CANDIDATE, 'Candidate'),
        (RECRUITER, 'Recruiter'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CANDIDATE)

    # add any other common fields here

    def is_candidate(self):
        return self.role == self.CANDIDATE

    def is_recruiter(self):
        return self.role == self.RECRUITER


class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')
    name = models.CharField(max_length=150, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    headline = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=128, blank=True)
    bio = models.TextField(blank=True)
    # resume relationship will be separate (one-to-many if multiple resumes allowed)

    def __str__(self):
        return f"CandidateProfile({self.user.username})"


class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    name = models.CharField(max_length=150, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=128, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"RecruiterProfile({self.user.username})"


class Job(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Embeddings: prefer JSONField for structured storage, fallback to TextField
    if JSONField:
        embeddings = JSONField(null=True, blank=True, help_text="Store vector as list of floats")
    else:
        embeddings = models.TextField(null=True, blank=True, help_text="JSON string of embeddings")

    def __str__(self):
        return self.title


class Resume(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/', null=True, blank=True)  # optional file
    text = models.TextField(blank=True)  # extracted text from resume (OCR/parsing)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    if JSONField:
        embeddings = JSONField(null=True, blank=True)
    else:
        embeddings = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Resume({self.candidate.user.username}, {self.id})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewing', 'Reviewing'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    # Optional: store application-level embeddings (e.g., candidate-job similarity)
    if JSONField:
        embeddings = JSONField(null=True, blank=True)
    else:
        embeddings = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Application({self.candidate.user.username} -> {self.job.title})"


