from django.shortcuts import render, redirect
from ..forms import CreateUserForm, PErrorList
from ..models import User
from django.contrib.auth import login, get_user
from django.contrib.auth.hashers import make_password
from .confirm_email import confirm_email


def sign_up(request):
    user = get_user(request)
    if user.is_authenticated:
        return redirect("/")
    if request.POST:
        form = CreateUserForm(request.POST, error_class=PErrorList)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(confirm_email)
        else:
            context = {"form": form}
            return render(request, "signup.html", context)
    context = {"form": CreateUserForm}
    return render(request, "signup.html", context)
