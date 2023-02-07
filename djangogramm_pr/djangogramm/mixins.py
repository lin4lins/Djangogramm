from django.shortcuts import redirect
from django.urls import reverse_lazy

from djangogramm.models import Profile


class ProfileRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if len(list(Profile.objects.filter(user=request.user))) == 0:
            return redirect(reverse_lazy('profile-create'))
        return super().dispatch(request, *args, **kwargs)