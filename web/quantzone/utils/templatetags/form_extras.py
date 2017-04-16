from django import template


register = template.Library()


@register.inclusion_tag('forms/input_snippet.html')
def text_input(field, *args, **kwargs):

    try:
        input_type = kwargs['type']
    except KeyError:
        input_type = 'text'

    try:
        placeholder = kwargs['placeholder']
    except KeyError:
        placeholder = None

    try:
        no_label = kwargs['no_label']
    except KeyError:
        no_label = None

    return {
        'field': field,
        'placeholder': placeholder,
        'input_type': input_type,
        'no_label': no_label
    }


@register.inclusion_tag('forms/date_input_snippet.html')
def date_input(field, *args, **kwargs):
    return {
        'field': field,
        'placeholder': kwargs['placeholder']
    }


@register.inclusion_tag('forms/avatar_snippet.html')
def avatar_input(field, user, *args, **kwargs):
    return {
        'field': field,
        'user': user
    }
