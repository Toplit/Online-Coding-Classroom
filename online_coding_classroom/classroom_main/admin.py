from django.contrib import admin
from .models import ComputingClass, School, Progress, Awards
from lesson.models import Lesson, Language, LessonHint

# Register your models here.

admin.site.register(ComputingClass)
admin.site.register(School)
admin.site.register(Lesson)
admin.site.register(Language)
admin.site.register(LessonHint)
admin.site.register(Progress)
admin.site.register(Awards)
