from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from djangogramm.models import Post


class FeedView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/feed.html'

    def get(self, request):
        posts = Post.objects.order_by('-created_at')
        return render(request, self.template_name, {'posts': posts})