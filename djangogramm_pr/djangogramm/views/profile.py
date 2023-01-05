from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from djangogramm.forms import ProfileForm
from djangogramm.models import Profile, Post


# Create your views here


class ProfileCreateView(LoginRequiredMixin, View):
    form = ProfileForm
    login_url = '/auth/login'

    def get(self, request):
        return render(request, 'djangogramm/profile_create.html', {'form': ProfileForm})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = self.request.user
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect('/profile/')


class ProfileView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(author = request.user).order_by('-publication_datetime')
        return render(request, 'djangogramm/profile.html', {'profile': profile, 'posts': posts})


class ProfileUpdateView(LoginRequiredMixin, View):
    form = ProfileForm
    login_url = '/auth/login'

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        filled_form = self.form(initial={'full_name': profile.full_name,
                                               'bio': profile.bio,
                                               'avatar': profile.avatar})
        return render(request, 'djangogramm/profile_update.html', {'form': filled_form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)

        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.full_name = form.cleaned_data['full_name']
            profile.bio = form.cleaned_data['bio']
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect('/profile')

