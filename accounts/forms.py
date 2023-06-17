from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        "placeholder": "Enter password",
        "class": "form-control"
    }))

    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "phone_number", "email", "password",)

    def __init__(self, *args, **kwatgs):
        super(RegistrationForm, self).__init__(*args, **kwatgs)

        self.fields["first_name"].widget.attrs["placeholder"] = "Enter first name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter last name"
        self.fields["email"].widget.attrs["placeholder"] = "Enter email address"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter phone number"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control" #form-control class for all of the registration fields
