from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Usuario


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        exclude = ["user"]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "validate",
                "id": "username",
                "type": "text",
            }),
            "email": forms.EmailInput(attrs={
                "class": "validate",
                "id": "email",
                "type": "text",
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "validate",
                "id": "password1",
                "type": "password",
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "validate",
                "id": "password2",
                "type": "password",
            })
        }


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "validate",
                "id": "username",
                "type": "text",
            }),
            "password": forms.PasswordInput(attrs={
                "class": "validate",
                "id": "password",
                "type": "password",
            })
        }
