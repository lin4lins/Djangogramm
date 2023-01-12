from django import forms

from djangogramm.models import Image, Post, Profile


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'avatar']


class PostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Post
        fields = ['caption']


class ImageForm(forms.ModelForm):
    original = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ['original']
