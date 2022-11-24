from django import forms
from django.contrib.auth.forms import UserCreationForm

from djangogramm.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ("email", "password1", "password2")

