from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from djangogramm.errors import InvalidFormException
from djangogramm.forms import ImageForm, PostForm
from djangogramm.models import Image, Post, Tag


class PostCreateView(LoginRequiredMixin, View):
    post_form = PostForm
    image_form = ImageForm
    login_url = "/auth/login"

    def get(self, request):
        return render(request, 'djangogramm/post_create.html', {"post_form": self.post_form,
                                                                "image_form": self.image_form})

    def post(self, request):
        user = request.user
        post_form = self.post_form(request.POST)
        images = request.FILES.getlist('image')

        post = self.__create_post(post_form, user)
        self.__create_images(images, post)
        self.__create_tags(post)
        return redirect('/')

    @staticmethod
    def __create_post(form: PostForm, user) -> Post:
        if form.is_valid():
            post_to_create = Post(author=user, caption=form.cleaned_data['caption'])
            post_to_create.save()
            return post_to_create

        raise InvalidFormException(form.errors)

    @staticmethod
    def __create_images(images: list, post: Post):
        for position, image in enumerate(images, 1):
                image_to_create = Image(post=post, image=image, preview=image, position=position)
                image_to_create.save()

    @staticmethod
    def __create_tags(post: Post):
        tags = PostCreateView.__get_tags_from_text(post.caption)
        for tag in tags:
            tag_to_create = Tag(name=tag)
            tag_to_create.save()
            tag_to_create.posts.add(post)
            tag_to_create.save()

    @staticmethod
    def __get_tags_from_text(text: str) -> list:
        return [word.replace("#", '') for word in text.split() if word[0] == "#"]