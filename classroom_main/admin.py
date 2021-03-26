from django.contrib import admin
from .models import ComputingClass, School, Progress, Awards
from lesson.models import Lesson, Language, LessonHint

# Models that are registered to be used on Admin site
admin.site.register(ComputingClass)
admin.site.register(School)
admin.site.register(Progress)
admin.site.register(Awards)
