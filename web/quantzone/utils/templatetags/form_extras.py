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
        'field': field
    }


@register.inclusion_tag('forms/select_snippet.html')
def select_input(field, *args, **kwargs):

    try:
        no_label = kwargs['no_label']
    except KeyError:
        no_label = None

    try:
        extra_class = kwargs['extra_class']
    except KeyError:
        extra_class = None

    return {
        'field': field,
        'no_label': no_label,
        'extra_class': extra_class
    }


@register.inclusion_tag('forms/avatar_snippet.html')
def avatar_input(field, user, *args, **kwargs):
    return {
        'field': field,
        'user': user
    }
