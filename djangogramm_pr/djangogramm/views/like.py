from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from djangogramm.models import Like, Post


class CreateLikeView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, post_id: int):
        liked_post = get_object_or_404(Post, id=post_id)
        try:
            Like.objects.get(post=liked_post, profile=request.user.profile)

        except Like.DoesNotExist:
            Like.objects.create(post=liked_post, profile=request.user.profile)
            return HttpResponse(status=201)

        else:
            return HttpResponse(status=404)



class DeleteLikeView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, post_id):
        disliked_post = get_object_or_404(Post, id=post_id)
        get_object_or_404(Like, post=disliked_post, profile=self.request.user.profile).delete()
        return HttpResponse(status=204)