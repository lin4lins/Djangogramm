from django import template

register = template.Library()

@register.simple_tag
def get_like(likes, user):
    for like in likes:
        if like.profile.user.id == user.id:
            return like