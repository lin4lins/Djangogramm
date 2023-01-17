from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from djangogramm.errors import InvalidFormException
from djangogramm.forms import ImageForm, PostForm
from djangogramm.models import Image, Post, Profile


class PostCreateView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/post_create.html'
    redirect_url = reverse_lazy('feed')

    def get(self, request):
        return render(request, self.template_name, {'post_form': PostForm, 'image_form': ImageForm})

    def post(self, request):
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)

        if not post_form.is_valid():
            raise InvalidFormException()

        if not image_form.is_valid():
            raise InvalidFormException()

        post = post_form.save(commit=False)
        post.author = get_object_or_404(Profile, user=request.user)
        post.save()

        self.__create_images(post, request.FILES.getlist('original'))

        return redirect(self.redirect_url)

    @staticmethod
    def __create_images(post: Post, image_list: list) -> None:
        for position, image in enumerate(image_list):
            Image(post=post, original=image, preview=image, position=position).save()


class PostDeleteView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_url = reverse_lazy('profile-me')

    def get(self, request, id):
        profile = get_object_or_404(Profile, user=request.user)
        get_object_or_404(Post, id=id, author=profile).delete()
        return redirect(self.redirect_url)
