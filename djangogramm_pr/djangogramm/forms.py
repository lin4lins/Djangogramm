from django import forms
from djangogramm.models import User


class EditProfileForm(forms.Form):
    full_name = forms.CharField(required=False, max_length=100)
    bio = forms.CharField(required=False, help_text="Tell us about you", max_length=255)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User

        fields = ["full_name", "bio", "avatar_path"]