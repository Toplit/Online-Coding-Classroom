from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('select-language/<str:environmentName>/', views.select_language, name="lesson-select-language"),
    path('select-env/', views.select_env, name="lesson-select-env"),
    path('select-lesson/<str:languageTitle>/', views.select_lesson, name="lesson-select-lesson"),
    url(r'get_code/$', views.compile_code, name="get_code"),
    path('lesson/<str:languageTitle>/<str:lessonTitle>/', views.lesson, name="lesson-lesson-specific"),
]
