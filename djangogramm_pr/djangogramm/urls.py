from django.urls import path

from djangogramm.views.post_views import PostCreateView
from djangogramm.views.profile_views import ProfileView, ProfileCreateView, ProfileUpdateView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/create', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/update', ProfileUpdateView.as_view(), name="profile-update"),
    path('post/create', PostCreateView.as_view(), name='post-create'),
    path('post/<id>/delete', PostDeleteView.as_view(), name='post-delete'),
]