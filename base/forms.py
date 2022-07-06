from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "mobile")

    def __init__(self, *args, **kwargs):
        """
        sets the limit for the mobile field in the form to 10 digits
        """
        super().__init__(*args, **kwargs)
        self.fields["mobile"] = forms.IntegerField(
            min_value=1000000000, max_value=9999999999
        )


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()
