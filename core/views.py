from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CandidateSignupForm, RecruiterSignupForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .utils import recruiter_required, candidate_required

@login_required
@recruiter_required
def recruiter_dashboard(request):
    return render(request, "core/recruiter_dashboard.html")


@login_required
@candidate_required
def candidate_dashboard(request):
    return render(request, "core/candidate_dashboard.html")

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
