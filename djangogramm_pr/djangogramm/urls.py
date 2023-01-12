from django.urls import path

from djangogramm.views.feed import FeedView
from djangogramm.views.like import CreateLikeView, DeleteLikeView
from djangogramm.views.post import PostCreateView, PostDeleteView
from djangogramm.views.profile import (ProfileCreateView, ProfileMeView,
                                       ProfileUpdateView, ProfileView)
from djangogramm.views.tag import SearchTagView

urlpatterns = [
    path('profile/create', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/update', ProfileUpdateView.as_view(), name="profile-update"),
    path('profile/me', ProfileMeView.as_view(), name="profile-me"),
    path('profile/<username>', ProfileView.as_view(), name="profile"),
    path('post/create', PostCreateView.as_view(), name='post-create'),
    path('post/<id>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:post_id>/create', CreateLikeView.as_view(), name='like-create'),
    path('like/<int:post_id>/delete', DeleteLikeView.as_view(), name='like-delete'),
    path('search/tag/<name>', SearchTagView.as_view(), name='tag'),
    path('', FeedView.as_view(), name='feed'),
]