from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from djangogramm.errors import InvalidFormException
from djangogramm.forms import ImageForm, PostForm
from djangogramm.models import Image, Post


class PostCreateView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/post_create.html'
    redirect_url = reverse_lazy('feed')

    def get(self, request):
        return render(request, self.template_name, {'post_form': PostForm, 'image_form': ImageForm})

    def post(self, request):
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)

        try:
            if not post_form.is_valid():
                raise InvalidFormException(form=post_form)

            if not image_form.is_valid():
                raise InvalidFormException(form=image_form)

            post = post_form.save(commit=False)
            post.author = request.user.profile
            post.save()

            for position, image in enumerate(request.FILES.getlist('original')):
                Image(post=post, original=image, preview=image, position=position).save()

            return redirect(self.redirect_url)

        except InvalidFormException as exc:
            error_messages = [message for message in exc.form.errors.values()]
            return render(request, 'errors.html', {'error_messages': error_messages})

class PostDeleteView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_url = reverse_lazy('profile-me')

    def get(self, request, id: int):
        get_object_or_404(Post, id=id, author=request.user.profile).delete()
        return redirect(self.redirect_url)
