from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from djangogramm.models import Post, Profile


class FeedView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/feed.html'

    def get(self, request):
        get_object_or_404(Profile, user=request.user)
        posts = Post.objects.order_by('-created_at')
        return render(request, self.template_name, {'posts': posts})