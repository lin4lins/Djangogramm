from django import template

from djangogramm.models import Profile, Follower
from signup.models import User

register = template.Library()


@register.simple_tag
def is_followed_by_current_user(current_user: User, profile: Profile) -> bool:
    try:
        Follower.objects.get(who_follows=current_user.profile, who_is_followed=profile)
        return True

    except Follower.DoesNotExist:
        return False