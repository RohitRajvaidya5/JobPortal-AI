from django.urls import path
from . import views # candidate_signup, recruiter_signup, login_view, logout_view, home

urlpatterns = [
    path("signup/candidate/", views.candidate_signup, name="candidate_signup"),
    path("signup/recruiter/", views.recruiter_signup, name="recruiter_signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home" ),
     path("redirect/", views.redirect_after_login, name="redirect_after_login"),
    path("candidate/dashboard/", views.candidate_dashboard, name="candidate_dashboard"),
    path("recruiter/dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
]
