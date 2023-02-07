from django import template

register = template.Library()

@register.simple_tag
def get_profile(profiles, post_author):
    for profile in profiles:
        if profile == post_author:
            return profile