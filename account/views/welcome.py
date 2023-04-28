from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def welcome(request):
    user = get_user(request)
    context = {"user": user}
    return render(request, "welcome.html", context=context)
