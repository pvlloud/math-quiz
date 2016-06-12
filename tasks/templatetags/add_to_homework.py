from django import template
from classes.models import Teacher

register = template.Library()


@register.inclusion_tag('tasks/templatetags/add_task.html', takes_context=True)
def add_task(context, task):
    homework = None
    try:
        this_user = context['user'].teacher
        homework = this_user.get_open_homework()
        show = bool(homework)
        if show:
            show = task not in homework.tasks.all()
    except Teacher.DoesNotExist:
        show = False

    return {'show': show,
            'task': task,
            'homework': homework}
