from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class CandidateSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.CANDIDATE
        if commit:
            user.save()
        return user


class RecruiterSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.RECRUITER
        if commit:
            user.save()
        return user
