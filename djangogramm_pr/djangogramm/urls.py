from django.urls import path

from djangogramm.views import ProfileCreateView, ProfileView, ProfileUpdateView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/create', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/update', ProfileUpdateView.as_view(), name="profile-update"),
]