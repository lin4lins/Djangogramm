from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from djangogramm.models import Post


class FeedView(LoginRequiredMixin, View):
    model = Post
    login_url = "/auth/login"
    template_name = 'djangogramm/feed.html'

    def get(self, request):
        posts = self.model.objects.order_by('-created_at')[:50]

        return render(request, self.template_name, {'posts': posts})