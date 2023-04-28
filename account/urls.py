from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import sign_up, log_in, log_out, confirm_email, welcome

urlpatterns = [
    path("signup/", sign_up, name="signup"),
    path("confirm/", confirm_email, name="confirm"),
    path("welcome/", welcome, name="welcome"),
    path("logout/", log_out, name="logout"),
    path("login/", log_in, name="login"),
]
