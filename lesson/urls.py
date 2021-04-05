from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('select-language/<str:environmentName>/', views.select_language, name="lesson-select-language"),   # Url for Select Language
    path('select-env/', views.select_env, name="lesson-select-env"),                                        # Url for Select Environment
    path('select-lesson/<str:languageTitle>/', views.select_lesson, name="lesson-select-lesson"),           # Url for Select Lesson
    url(r'get_code/$', views.compile_code, name="get_code"),                                                # Url for retrieving user submitted code
    path('lesson/<str:languageTitle>/<str:lessonTitle>/', views.lesson, name="lesson-lesson-specific"),     # Url for lesson page
    path('lesson/completed/<str:languageTitle>', views.language_complete, name="lesson-language-complete"),
    path('lesson/<str:languageTitle>/<str:currentLessonTitle>/<str:nextLessonTitle>/', views.next_lesson, name="lesson-next-lesson"),
]
