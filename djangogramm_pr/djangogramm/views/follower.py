from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from djangogramm.models import Follower, Profile
from signup.models import User


class CreateFollowView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, username: str):
        user_to_to_follow = get_object_or_404(User, username=username)
        profile_to_follow = get_object_or_404(Profile, user=user_to_to_follow)
        try:
            Follower.objects.get(who_follows=request.user.profile, who_is_followed=profile_to_follow)

        except Follower.DoesNotExist:
            Follower.objects.create(who_follows=request.user.profile, who_is_followed=profile_to_follow)
            return HttpResponse(status=201)

        except User.profile.RelatedObjectDoesNotExist:
            return HttpResponse(status=404)

        else:
            return HttpResponse(status=404)


class DeleteFollowView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def post(self, request, username: str):
        user_to_unfollow = get_object_or_404(User, username=username)
        profile_to_unfollow = get_object_or_404(Profile, user=user_to_unfollow)
        try:
            get_object_or_404(Follower, who_follows=request.user.profile, who_is_followed=profile_to_unfollow).delete()

        except User.profile.RelatedObjectDoesNotExist:
            return HttpResponse(status=404)

        else:
            return HttpResponse(status=204)
