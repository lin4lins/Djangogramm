from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from djangogramm.forms import ProfileForm
from djangogramm.models import Follower, Like, Post, Profile
from signup.models import User

# Create your views here


class ProfileCreateView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile_create.html'
    redirect_url = reverse_lazy('profile-me')

    def get(self, request):
        return render(request, self.template_name, {'form': ProfileForm})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = self.request.user
                profile.save()
                return redirect(self.redirect_url)

            return render(request, 'signup/signup.html', {'form': form})

        except IntegrityError:
            return HttpResponse(status=405)


class ProfileView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile.html'

    def get(self, request, username):
        user =  User.objects.get(username=username)
        if user == request.user:
            return redirect(reverse_lazy('profile-me'))

        current_profile = Profile.objects.select_related('user').get(user=request.user)
        profile = Profile.objects.select_related('user').get(user=user)
        posts = Post.objects.prefetch_related('tags', 'media', 'likes').filter(author=profile)
        likes = Like.objects.select_related().filter(post__in=posts)
        followers = Follower.objects.select_related().filter(who_is_followed=profile)
        following = Follower.objects.select_related().filter(who_follows=profile)

        return render(request, self.template_name, {'current_profile': current_profile, 'profile': profile,
                                                    'posts': posts, 'likes': likes,
                                                   'followers': followers, 'following_profiles': following})


class ProfileMeView(LoginRequiredMixin, View):
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


class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile_update.html'
    redirect_url = reverse_lazy('profile-me')

    def get(self, request):
        current_profile = Profile.objects.select_related('user').get(user=request.user)
        filled_form = ProfileForm(initial={'full_name': current_profile.full_name, 'bio': current_profile.bio,
                                           'avatar': current_profile.avatar})
        return render(request, self.template_name, {'current_profile': current_profile, 'form': filled_form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = get_object_or_404(Profile, user=request.user)
            profile.full_name = form.cleaned_data['full_name']
            profile.bio = form.cleaned_data['bio']
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect(self.redirect_url)

        return render(request, self.template_name, {'form': ProfileForm})