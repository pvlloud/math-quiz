from django import template
from tasks.models import Category

register = template.Library()


@register.inclusion_tag('tasks/templatetags/all_categories.html')
def all_categories():
    categories = Category.objects.all()
    return {'categories': categories}
