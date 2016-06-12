from django import template


register = template.Library()


@register.inclusion_tag('tasks/templatetags/levels.html')
def category_levels(category):
    return {'category': category}
