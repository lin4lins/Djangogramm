from django import template

from djangogramm.models import Profile

register = template.Library()

@register.simple_tag
def get_like(current_profile: Profile, likes: list):
    for like in likes:
        if like.profile == current_profile:
            return like