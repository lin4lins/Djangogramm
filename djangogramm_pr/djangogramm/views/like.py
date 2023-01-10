from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from ast import literal_eval

from djangogramm.models import Like, Post, Profile


class CreateLikeView(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def post(self, request, post_id: int):
        liked_post = get_object_or_404(Post, id=post_id)
        liked_by = get_object_or_404(Profile, user_id=request.user.id)
        Like(post=liked_post, profile=liked_by).save()
        return HttpResponse(status=201)


class DeleteLikeView(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def post(self, request, post_id):
        disliked_post = get_object_or_404(Post, id=post_id)
        disliked_by = get_object_or_404(Profile, user_id=request.user.id)
        Like.objects.filter(post=disliked_post, profile=disliked_by).delete()
        return HttpResponse(status=204)