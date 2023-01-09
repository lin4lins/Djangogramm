from django.urls import path

from djangogramm.views.feed import FeedView
from djangogramm.views.post import PostCreateView, PostDeleteView
from djangogramm.views.profile import ProfileView, ProfileMeView, ProfileCreateView, ProfileUpdateView

urlpatterns = [
    path('profile/create', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/update', ProfileUpdateView.as_view(), name="profile-update"),
    path('profile/me', ProfileMeView.as_view(), name="profile-me"),
    path('profile/<id>', ProfileView.as_view(), name="profile"),
    path('post/create', PostCreateView.as_view(), name='post-create'),
    path('post/<id>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('', FeedView.as_view(), name='feed'),
]