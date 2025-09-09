from django import template


register = template.Library()
cursed_words = ['max', 'Max', 'MAX', 'блять', 'пиздец']


@register.filter()
def censore(value):
    updated_body = ''
    for word in cursed_words:
        if updated_body:
            updated_body = updated_body.replace(word, f'{'*' * len(word)}')
        else:
            updated_body = value.replace(word, f'{'*' * len(word)}')
    return updated_body
