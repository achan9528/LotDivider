from django import template

register = template.Library()

@register.filter
def getType(something):
    print(type(something))
    return(type(something))