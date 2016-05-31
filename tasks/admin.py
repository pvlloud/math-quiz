from django.contrib import admin
from models import Task, Attempt, Category, TheoryEntry, SolvedTask

# Register your models here.
admin.site.register(Task)
admin.site.register(Attempt)
admin.site.register(Category)
admin.site.register(SolvedTask)
admin.site.register(TheoryEntry)
