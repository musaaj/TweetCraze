from django.shortcuts import render, redirect
from django.contrib.auth import get_user


def index(request):
    user = get_user(request)
    if user.is_authenticated:
        return redirect("dashboard/")
    return render(request, "index.html", context={})
