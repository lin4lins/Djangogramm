from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_caption_with_tags(caption: str) -> str:
    words_with_links = []
    for word in caption.split():
        if word[0] == '#':
            slug = word[1:]
            words_with_links.append(f'<a href=/search/tag/{slug}>{word}</a>')
        else:
            words_with_links.append(word)

    return mark_safe(' '.join(words_with_links))
