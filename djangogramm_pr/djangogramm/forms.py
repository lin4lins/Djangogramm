from django import forms
from djangogramm.models import Profile, Post, Image, Tag


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ["full_name", "bio", "avatar"]


class PostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Post
        fields = ["caption"]

    def save(self, commit=True):
        post_to_save = super().save(commit=False)
        self.__create_tags(post_to_save)

        if commit:
            post_to_save.save()

        return post_to_save

    @staticmethod
    def __create_tags(post: Post):
        for tag in post.get_tags_text_from_caption():
            if not Tag.objects.filter(name=tag):
                tag_to_create = Tag(name=tag)
                tag_to_create.save()
                tag_to_create.posts.add(post)
                tag_to_create.save()


class ImageForm(forms.ModelForm):
    original = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ["original"]
