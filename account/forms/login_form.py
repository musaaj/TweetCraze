from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model
from django import forms


class LoginForm(forms.Form):
    error_css_class = "text-danger"
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control form-control-lg"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=256,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg"}),
    )
    error_messages = {
        "invalid_login": ("Please enter a valid email and password"),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)
        userModel = get_user_model()
        self.email_field = userModel._meta.get_field(userModel.USERNAME_FIELD)
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    message="Invalid login credentials",
                    code="invalid_login",
                    params={
                        "email": self.email_field.verbose_name,
                    },
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        pass
