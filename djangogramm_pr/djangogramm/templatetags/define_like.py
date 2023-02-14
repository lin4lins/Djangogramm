from django import template

from djangogramm.models import Profile, Post

register = template.Library()

@register.simple_tag
def get_like(current_profile: Profile, likes: list, post: Post):
    for like in likes:
        if like.profile == current_profile and like.post == post:
            return True