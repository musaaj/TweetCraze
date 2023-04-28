from django import forms
from django.contrib.auth.hashers import make_password
from django.forms.utils import ErrorList
from django.contrib.auth import get_user_model


class PErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return "".join(['<p class="text-danger">%s</p>' % e for e in self])


class CreateUserForm(forms.ModelForm):
    def __init__(
        self,
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=PErrorList,
        label_suffix=None,
        empty_permitted=False,
        instance=None,
        use_required_attribute=None,
        renderer=None,
    ):
        super().__init__(
            data,
            files,
            auto_id,
            prefix,
            initial,
            error_class,
            label_suffix,
            empty_permitted,
            instance,
            use_required_attribute,
            renderer,
        )
        self.model = get_user_model()

    class Meta:
        model = get_user_model()
        error_css_class = "text-danger"
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control form-control-lg", "type": "email"}
            ),
            "password": forms.TextInput(
                attrs={"class": "form-control form-control-lg", "type": "text"}
            ),
        }
        error_messages = {
            "email": {
                "unique": "User with this email already exists",
            }
        }

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            self.add_error(
                "password", "Password too short: Must be more than 7 characters."
            )
        elif self.model.objects.filter(email=email):
            self.add_error("email", "User with this email already exist")
        else:
            return self.cleaned_data

    def save(self, commit=True):
        self.instance.password = make_password(self.instance.password)
        if commit:
            self.instance.save()
        return self.instance
