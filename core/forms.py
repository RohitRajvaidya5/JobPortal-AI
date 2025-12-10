from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, CandidateProfile, RecruiterProfile, Resume

class CandidateSignupForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=False)
    surname = forms.CharField(max_length=150, required=False)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.CANDIDATE
        if commit:
            user.save()

            # set profile name/surname (signals create profile on save)
            try:
                profile = user.candidate_profile
            except Exception:
                profile, _ = CandidateProfile.objects.get_or_create(user=user)

            profile.name = self.cleaned_data.get('name', '')
            profile.surname = self.cleaned_data.get('surname', '')
            profile.save()

        return user


class RecruiterSignupForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=False)
    surname = forms.CharField(max_length=150, required=False)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.RECRUITER
        if commit:
            user.save()

            try:
                profile = user.recruiter_profile
            except Exception:
                profile, _ = RecruiterProfile.objects.get_or_create(user=user)

            profile.name = self.cleaned_data.get('name', '')
            profile.surname = self.cleaned_data.get('surname', '')
            profile.save()

        return user
    


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["file"]

