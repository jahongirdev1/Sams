from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_current(context, lang_code: str):
    request = context["request"]
    return translate_url(request.build_absolute_uri(), lang_code)