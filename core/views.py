from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CandidateSignupForm, RecruiterSignupForm
from django.http import HttpResponse

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
        return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")
