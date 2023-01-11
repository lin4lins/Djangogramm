from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from djangogramm.errors import InvalidFormException
from djangogramm.forms import ImageForm, PostForm
from djangogramm.models import Post, Profile, Image


class PostCreateView(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        return render(request, 'djangogramm/post_create.html', {"post_form": PostForm,
                                                                "image_form": ImageForm})

    def post(self, request):
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)

        if not post_form.is_valid():
            raise InvalidFormException(post_form.errors)

        if not image_form.is_valid():
            raise InvalidFormException(image_form.errors)

        post = post_form.save(commit=False)
        post.author = Profile.objects.get(user=request.user)
        post.save()

        for position, image in enumerate(request.FILES.getlist('original')):
            image_to_create = Image(post=post, original=image, preview=image, position=position)
            image_to_create.save()

        return redirect('/')


class PostDeleteView(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request, id):
        profile = Profile.objects.get(user=request.user)
        Post.objects.filter(id=id, author=profile).delete()
        return redirect('/profile/me')
