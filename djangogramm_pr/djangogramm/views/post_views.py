from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from djangogramm.forms import PostForm, ImageForm, TagForm


class PostCreateView(LoginRequiredMixin, View):
    login_url = "/auth/login"
    post_form = PostForm
    image_form = ImageForm
    tag_form = TagForm

    def get(self, request):
        return render(request, 'djangogramm/post_create.html', {"post_form": self.post_form,
                                                                "image_form": self.image_form,
                                                                "tag_form": self.tag_form})

    def post(self, request):
        post = PostForm(request.POST)
        images = ImageForm(request.FILES)
        tags = TagForm(request.POST)
        print(post)
        # print(dict(request.POST.items()))
