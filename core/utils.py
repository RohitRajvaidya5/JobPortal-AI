from django.http import HttpResponseForbidden

def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect("login")

        if request.user.role != "recruiter":
            return HttpResponseForbidden("You are not allowed to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def candidate_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect("login")

        if request.user.role != "candidate":
            return HttpResponseForbidden("You are not allowed to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
