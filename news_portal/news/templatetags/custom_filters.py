from django import template

register = template.Library()

replacements = {
    'dolor': 'd****',
    'Dolor': 'D****',
    'ips': 'i**',
    'Ips': 'I**'
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    text = value
    for r in replacements.items():
        text = text.replace(r[0], r[1])
    return text
