from django import forms
from djangogramm.models import Profile, Post, Image


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ["full_name", "bio", "avatar"]


class PostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ["caption"]


class ImageForm(forms.ModelForm):
    file = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ["image"]
