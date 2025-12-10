from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CandidateSignupForm, RecruiterSignupForm
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .utils import recruiter_required, candidate_required
from .forms import ResumeUploadForm
from accounts.models import Resume, CandidateProfile, RecruiterProfile
from django.shortcuts import render, redirect, get_object_or_404

@login_required
@recruiter_required
def recruiter_dashboard(request):
    recruiter_profile = get_object_or_404(RecruiterProfile, user=request.user)
    # TODO: add real stats/context later
    return render(request, "core/recruiter_dashboard.html", {"recruiter_profile": recruiter_profile})


@login_required
def candidate_dashboard(request):
    candidate_profile = get_object_or_404(CandidateProfile, user=request.user)
    resumes = candidate_profile.resumes.all()
    return render(request, "core/candidate_dashboard.html", {"resumes": resumes, "candidate_profile": candidate_profile})

@login_required
def redirect_after_login(request):
    if request.user.role == "candidate":
        return redirect("candidate_dashboard")
    elif request.user.role == "recruiter":
        return redirect("recruiter_dashboard")
    return redirect("login")


def home(request):
    return render(request, "core/home.html")


def candidate_signup(request):
    form = CandidateSignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, "core/candidate_signup.html", {"form": form})



def recruiter_signup(request):
    form = RecruiterSignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "core/recruiter_signup.html", {"form": form})


def login_view(request):
    
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)

        if user.role == "candidate":
            return redirect('candidate_dashboard')
        elif user.role == "recruiter":
            return redirect('recruiter_dashboard')
        else:
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")



@login_required
def upload_resume(request):
    # get candidate profile for the logged-in user
    candidate_profile = get_object_or_404(CandidateProfile, user=request.user)

    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.candidate = candidate_profile   # IMPORTANT FIX
            resume.save()
            return redirect("candidate_dashboard")
    else:
        form = ResumeUploadForm()

    return render(request, "core/upload_resume.html", {"form": form})


@login_required
@candidate_required
def delete_resume(request, pk):
    """Delete a resume owned by the logged-in candidate.

    Accepts POST only. Removes the file from storage (if present) and deletes
    the Resume object, then redirects back to the candidate dashboard.
    """
    if request.method != "POST":
        return redirect("candidate_dashboard")

    resume = get_object_or_404(Resume, pk=pk)

    # ensure the resume belongs to the requesting user
    if resume.candidate.user != request.user:
        return HttpResponseForbidden("You do not have permission to delete this resume.")

    # delete the underlying file from storage if present
    try:
        if resume.file:
            resume.file.delete(save=False)
    except Exception:
        # ignore file deletion errors, still attempt to delete DB record
        pass

    resume.delete()
    return redirect("candidate_dashboard")

