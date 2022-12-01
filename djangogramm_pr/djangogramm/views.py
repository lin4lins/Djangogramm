from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, TemplateView

from djangogramm.forms import ProfileForm
from djangogramm.models import Profile


# Create your views here


class ProfileCreateView(LoginRequiredMixin, View):
    form = ProfileForm
    login_url = "/auth/login"

    def get(self, request):
        return render(request, 'djangogramm/profile_create.html', {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = self.request.user
            profile.save()
            return redirect(f'/profile/')


class ProfileView(LoginRequiredMixin, View):
    model = Profile
    login_url = "/auth/login"

    def get(self, request):
        profile = self.model.objects.get(user=request.user)
        return render(request, 'djangogramm/profile.html', {'profile': profile})


class ProfileUpdateView(LoginRequiredMixin, View):
    model = Profile
    form = ProfileForm
    login_url = "/auth/login"

    def get(self, request):
        profile = self.model.objects.filter(user=request.user).first()
        filled_form = self.form(initial={'full_name': profile.full_name,
                                               'bio': profile.bio,
                                               'avatar': profile.avatar})
        return render(request, 'djangogramm/profile_update.html', {'form': filled_form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            profile = self.model.objects.filter(user=request.user).first()
            profile.full_name = form.cleaned_data['full_name']
            profile.bio = form.cleaned_data['bio']
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect(f'/profile/')

