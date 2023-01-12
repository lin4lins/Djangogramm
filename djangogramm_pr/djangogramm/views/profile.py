from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from djangogramm.forms import ProfileForm
from djangogramm.models import Post, Profile
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

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = self.request.user
            profile.save()
            return redirect(self.redirect_url)


class ProfileView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile =  get_object_or_404(Profile, user=user)
        posts = Post.objects.filter(author=profile).order_by('-created_at')
        return render(request, self.template_name, {'profile': profile, 'posts': posts})

class ProfileMeView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile-me.html'

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        posts = Post.objects.filter(author=profile).order_by('-created_at')
        return render(request, self.template_name, {'profile': profile, 'posts': posts})

class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    template_name = 'djangogramm/profile_update.html'
    redirect_url = reverse_lazy('profile-me')

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        filled_form = ProfileForm(initial={'full_name': profile.full_name,
                                               'bio': profile.bio,
                                               'avatar': profile.avatar})
        return render(request, self.template_name, {'form': filled_form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = get_object_or_404(Profile, user=request.user)
            profile.full_name = form.cleaned_data['full_name']
            profile.bio = form.cleaned_data['bio']
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect(self.redirect_url)
