from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="highlight_word")
def highlight_word(text, word):
    """
    Wraps the first occurrence of `word` inside `text` with a styled span,
    keeping it in its correct position (unlike |cut, which strips the word
    out and can't put it back where it belonged).
    """
    if not text:
        return ""
    if not word:
        return escape(text)

    index = text.find(word)
    if index == -1:
        return escape(text)

    before = escape(text[:index])
    match = escape(text[index:index + len(word)])
    after = escape(text[index + len(word):])

    return mark_safe(f'{before}<span class="highlight-word">{match}</span>{after}')