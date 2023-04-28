from django import forms


class ConfirmEmailForm(forms.Form):
    code = forms.CharField(
        label="Type the 6-digit code here",
        max_length=6,
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "489345"}
        ),
    )
