from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.views import View
from djangogramm.models import Like, Post, Profile


class CreateLikeView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, post_id: int):
        try:
            liked_post = get_object_or_404(Post, id=post_id)
            liked_by = get_object_or_404(Profile, user_id=request.user.id)
            Like.objects.create(post=liked_post, profile=liked_by)
            return HttpResponse(status=201)

        except IntegrityError:
            return HttpResponse(status=404)


class DeleteLikeView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, post_id):
        try:
            disliked_post = get_object_or_404(Post, id=post_id)
            disliked_by = get_object_or_404(Profile, user_id=request.user.id)
            get_object_or_404(Like, post=disliked_post, profile=disliked_by).delete()
            return HttpResponse(status=204)

        except IntegrityError:
            return HttpResponse(status=404)
