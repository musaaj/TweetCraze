from django.shortcuts import render, redirect
from ..forms import LoginForm
from ..models import User
from django.contrib.auth import login, get_user, authenticate


def log_in(request):
    error = None
    user = get_user(request)
    if user.is_authenticated:
        return redirect("/")
    if request.POST:
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        else:
            context = {
                "form": form,
            }
            return render(request, "signin.html", context=context)
    context = {"form": LoginForm}
    return render(request, "signin.html", context=context)
