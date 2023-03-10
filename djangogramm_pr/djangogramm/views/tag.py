from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from djangogramm.mixins import ProfileRequiredMixin
from djangogramm.models import Like, Post, Profile, Tag


class SearchTagView(LoginRequiredMixin, ProfileRequiredMixin, View):
    login_url = "/auth/login"
    template_name = 'djangogramm/tag.html'

    def get(self, request, name: str):
        tag = get_object_or_404(Tag, name=name)

        current_profile = Profile.objects.select_related('user').get(user=request.user)
        profiles = Profile.objects.select_related('user').all()
        posts = Post.objects.select_related().prefetch_related('tags', 'media', 'likes').filter(tags=tag).order_by('-created_at')
        likes = Like.objects.select_related().filter(post__in=posts)
        return render(request, self.template_name, {'current_profile': current_profile, 'tag': tag, 'posts': posts,
                                                    'profiles': profiles, 'likes': likes})


