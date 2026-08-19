from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "Your name",
            "username": "Choose a username",
            "email": "you@example.com",
            "password1": "Create a password",
            "password2": "Confirm password",
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "input-field",
                "placeholder": placeholders.get(name, ""),
            })
