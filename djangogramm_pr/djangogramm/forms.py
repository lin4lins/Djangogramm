from django import forms
from djangogramm.models import Profile


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(required=False, max_length=100)
    bio = forms.CharField(required=False, help_text="Tell us about you", max_length=255)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ["full_name", "bio", "avatar"]


class PostForm(forms.ModelForm):
    caption = forms.CharField(required=False, max_length=255)

    class Meta:
        model = Post
        fields = ["caption"]


class ImageForm(forms.ModelForm):
    file = forms.ImageField(label="Images", required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))


    class Meta:
        model = Image
        fields = ["file"]


class TagForm(forms.ModelForm):
    name = forms.CharField(label="Tags", required=False)

    class Meta:
        model = Image
        fields = ["name"]

