from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from djangogramm.mixins import ProfileRequiredMixin
from djangogramm.models import Follower, Profile
from signup.models import User


class CreateFollowView(LoginRequiredMixin, ProfileRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, username: str):
        user_to_to_follow = User.objects.get(username=username)
        profile_to_follow = Profile.objects.get(user=user_to_to_follow)
        try:
            Follower.objects.get(who_follows=request.user.profile, who_is_followed=profile_to_follow)

        except Follower.DoesNotExist:
            Follower.objects.create(who_follows=request.user.profile, who_is_followed=profile_to_follow)
            return HttpResponse(status=201)

        else:
            return HttpResponse(status=404)


class DeleteFollowView(LoginRequiredMixin, ProfileRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, username: str):
        user_to_unfollow = User.objects.get(username=username)
        profile_to_unfollow = Profile.objects.get(user=user_to_unfollow)
        get_object_or_404(Follower, who_follows=request.user.profile, who_is_followed=profile_to_unfollow).delete()
        return HttpResponse(status=204)
