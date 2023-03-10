from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from djangogramm.errors import InvalidFormException
from djangogramm.forms import ProfileForm
from djangogramm.mixins import ProfileRequiredMixin
from djangogramm.models import Follower, Like, Post, Profile
from signup.models import User

# Create your views here


class ProfileCreateView(LoginRequiredMixin, View):
    url = reverse_lazy('profile-create')
    login_url = '/auth/login'
    template_name = 'djangogramm/profile_create.html'
    redirect_url = reverse_lazy('profile-me')

    def get(self, request):
        return render(request, self.template_name, {'form': ProfileForm})

    def post(self, request):
        try:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = self.request.user
                profile.save()
                return redirect(self.redirect_url)

            raise InvalidFormException(form=form)

        except InvalidFormException:
            return redirect(self.url)

        except IntegrityError:
            return HttpResponse(status=405)


class ProfileView(LoginRequiredMixin, ProfileRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile.html'

    def get(self, request, username):
        user =  get_object_or_404(User, username=username)
        if user == request.user:
            return redirect(reverse_lazy('profile-me'))

        try:
            profile = Profile.objects.select_related('user').get(user=user)

        except Profile.DoesNotExist:
            return HttpResponse(status=404)

        current_profile = Profile.objects.select_related('user').get(user=request.user)
        posts = Post.objects.prefetch_related('tags', 'media', 'likes').filter(author=profile)
        likes = Like.objects.select_related().filter(post__in=posts)
        followers = Follower.objects.select_related().filter(who_is_followed=profile)
        following = Follower.objects.select_related().filter(who_follows=profile)

        return render(request, self.template_name, {'current_profile': current_profile, 'profile': profile,
                                                    'posts': posts, 'likes': likes,
                                                   'followers': followers, 'following_profiles': following})


class ProfileMeView(LoginRequiredMixin, ProfileRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile-me.html'

    def get(self, request):
        current_profile =  Profile.objects.select_related('user').prefetch_related().get(user=request.user)
        posts = Post.objects.prefetch_related('tags', 'media', 'likes').filter(author=current_profile)
        likes = Like.objects.select_related().filter(post__in=posts)
        followers = Follower.objects.select_related().filter(who_is_followed=current_profile)
        following = Follower.objects.select_related().filter(who_follows=current_profile)

        return render(request, self.template_name, {'current_profile': current_profile, 'posts': posts, 'likes': likes,
                                                    'followers': followers, 'following_profiles': following})


class ProfileUpdateView(LoginRequiredMixin, ProfileRequiredMixin, View):
    url = reverse_lazy('profile-update')
    login_url = '/auth/login'
    template_name = 'djangogramm/profile_update.html'
    redirect_url = reverse_lazy('profile-me')

    def get(self, request):
        current_profile = Profile.objects.select_related('user').get(user=request.user)
        filled_form = ProfileForm(initial={'full_name': current_profile.full_name, 'bio': current_profile.bio,
                                           'avatar': current_profile.avatar})
        return render(request, self.template_name, {'current_profile': current_profile, 'form': filled_form})

    def post(self, request):
        try:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = get_object_or_404(Profile, user=request.user)
                profile.full_name = form.cleaned_data['full_name']
                profile.bio = form.cleaned_data['bio']
                profile.avatar = form.cleaned_data['avatar'] if form.cleaned_data['avatar'] else None
                profile.save()
                return redirect(self.redirect_url)

            raise InvalidFormException(form=form)

        except InvalidFormException:
            return redirect(self.url)