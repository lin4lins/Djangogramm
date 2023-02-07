from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from djangogramm.models import Like, Post, Profile, Tag


class SearchTagView(LoginRequiredMixin, View):
    login_url = "/auth/login"
    template_name = 'djangogramm/tag.html'

    def get(self, request, name: str):
        current_profile = Profile.objects.select_related('user').get(user=request.user)
        profiles = Profile.objects.select_related('user').all()
        tag = Tag.objects.get(name=name)
        posts = Post.objects.select_related().prefetch_related('tags', 'media', 'likes').filter(tags=tag).order_by('-created_at')
        likes = Like.objects.select_related().filter(post__in=posts)
        return render(request, self.template_name, {'current_profile': current_profile, 'tag': tag, 'posts': posts,
                                                    'profiles': profiles, 'likes': likes})


