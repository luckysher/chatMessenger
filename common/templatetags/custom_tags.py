from django import template

register = template.Library()


@register.filter(name='getuser')
def getuser(request):
    return request.__dict__['user'].get_full_name()
