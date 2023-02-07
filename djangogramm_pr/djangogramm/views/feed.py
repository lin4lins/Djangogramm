from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from djangogramm.mixins import ProfileRequiredMixin
from djangogramm.models import Like, Post, Profile


class FeedView(LoginRequiredMixin, ProfileRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/feed.html'

    def get(self, request):
        current_profile = Profile.objects.select_related('user').get(user=request.user)
        profiles = Profile.objects.select_related('user').all()
        posts = Post.objects.select_related().prefetch_related('tags', 'media', 'likes').order_by('-created_at')
        likes = Like.objects.select_related().filter(post__in=posts)
        return render(request, self.template_name, {'current_profile': current_profile, 'posts': posts,
                                                    'profiles': profiles, 'likes':likes})
