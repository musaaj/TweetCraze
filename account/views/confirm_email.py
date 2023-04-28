from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from ..forms import ConfirmEmailForm
from ..mail.mail_sender import send_confirmation_link
from ..models import ConfirmEmailModel
from django.contrib.auth import login, get_user, logout
from ..code import rand_code
from .welcome import welcome


def confirm_email(request):
    if request.GET and request.GET.get("code"):
        code = request.GET["code"]
        try:
            user_code = ConfirmEmailModel.objects.get(code=code)
            user = user_code.user
            user_code.delete()
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(welcome)
        except ConfirmEmailModel.DoesNotExist:
            return HttpResponseBadRequest("Forbidden request!")
    if request.POST:
        form = ConfirmEmailForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            try:
                user_code = ConfirmEmailModel.objects.get(code=code)
                user = user_code.user
                user.is_active = True
                user.save()
                login(request, user)
                user_code.delete()
                return redirect(welcome)
            except ConfirmEmailModel.DoesNotExist:
                context = {"form": form, "error": "Invalid code"}
                return render(request, "confirm_email.html", context=context)
    context = {"form": ConfirmEmailForm()}
    user = get_user(request)
    user_code = ConfirmEmailModel()
    user_code.code = rand_code()
    user_code.user = user
    user_code.save()
    send_confirmation_link(user.email, user_code.code)
    logout(request)
    return render(request, "confirm_email.html", context=context)
