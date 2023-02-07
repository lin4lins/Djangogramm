from django import template

from djangogramm.models import Profile

register = template.Library()


@register.simple_tag
def is_followed_by_current_profile(current_profile: Profile, profile: Profile, followers: list) -> bool:
    for follower in followers:
        if follower.who_is_followed == profile and follower.who_follows == current_profile:
            return True

    return False