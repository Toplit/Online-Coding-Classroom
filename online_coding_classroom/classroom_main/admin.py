from django.contrib import admin
from .models import ComputingClass, School, Lesson, Language, LessonHint, Progress, Awards

# Register your models here.

admin.site.register(ComputingClass)
admin.site.register(School)
admin.site.register(Lesson)
admin.site.register(Language)
admin.site.register(LessonHint)
admin.site.register(Progress)
admin.site.register(Awards)
