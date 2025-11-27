from django.urls import path
from .views import candidate_signup, recruiter_signup, login_view, logout_view, home

urlpatterns = [
    path("signup/candidate/", candidate_signup, name="candidate_signup"),
    path("signup/recruiter/", recruiter_signup, name="recruiter_signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home" )
]
