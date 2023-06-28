from django import forms
from .models import Account, UserProfile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password

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

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )
        
        validate_password(password)

class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        "placeholder": "Create new password",
        "class": "form-control"
    }))

    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = Account
        fields = ("password",)

    def __init__(self, *args, **kwatgs):
        super(ResetPasswordForm, self).__init__(*args, **kwatgs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )
        
        validate_password(password)

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "phone_number",)

    def __init__(self, *args, **kwatgs):
        super(UserForm, self).__init__(*args, **kwatgs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {"invalid":("Image files only",)}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ("address_line_1", "address_line_2","city" ,"state", "country", "profile_picture",)

    def __init__(self, *args, **kwatgs):
        super(UserProfileForm, self).__init__(*args, **kwatgs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget = forms.PasswordInput(attrs={
        "placeholder": "Current password",
        "class": "form-control"
    }))

    new_password = forms.CharField(widget = forms.PasswordInput(attrs={
        "placeholder": "New password",
        "class": "form-control"
    }))

    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={
        "placeholder": "Confirm new password",
        "class": "form-control"
    }))

    def __init__(self, user, data=None):
        self.user = user
        super(ChangePasswordForm, self).__init__(data=data)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        password_valid = check_password(current_password, self.user.password)
        
        if new_password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )
        elif new_password == current_password:
            raise forms.ValidationError(
                "New password cannot be the same as current one. Try again!"
            )
        elif not password_valid:
            raise forms.ValidationError(
                "Current password is incorrect."
            )
        
        validate_password(new_password)




