from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import View
from djangogramm.models import Tag, Profile


class SearchTagView(LoginRequiredMixin, View):
    login_url = "/auth/login"
    template_name = 'djangogramm/tag.html'

    def get(self, request, name: str):
        profile = get_object_or_404(Profile, user=request.user)
        tag = get_object_or_404(Tag, name=name)
        return render(request, self.template_name, {'tag': tag})

