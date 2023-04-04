from django import template

register = template.Library()

replacements = {
    'Редиска': 'Ре*****',
    'редиска': 'ре*****'
}


@register.filter()
def censor(value):
    text = value
    for r in replacements.items():
        text = text.replace(r[0], r[1])
    return text
