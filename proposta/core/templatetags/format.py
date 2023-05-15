from django import template
import locale

register = template.Library()

@register.filter(name='format')
def format(value, fmt):
    return fmt.format(value)


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@register.filter
def currency(value):
    value = locale.currency(value, grouping=True, symbol='R$')
    return value