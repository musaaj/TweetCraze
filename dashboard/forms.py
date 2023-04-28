from django import forms


class DMForm(forms.Form):
    text = forms.CharField(
            label="Message:",
            widget=forms.Textarea(
                attrs={
                    "class": "form-control form-control-lg",
                    "rows":4,
                }
            )
        )
