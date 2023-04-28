from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth import get_user, logout
from .sign_in import log_in


@login_required
def log_out(request):
    user = get_user(request)
    if user.is_authenticated:
        logout(request)
    return redirect(log_in)
