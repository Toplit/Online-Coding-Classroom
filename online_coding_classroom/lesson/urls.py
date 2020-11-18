from django.urls import path
from . import views

urlpatterns = [
    path('select-language', views.select_language, name="lesson-select-language"),
    path('select-lesson', views.select_lesson, name="lesson-select-lesson"),
    path('lesson', views.lesson, name="lesson-lesson"), #Change URL to be dynamic for selected language
]
