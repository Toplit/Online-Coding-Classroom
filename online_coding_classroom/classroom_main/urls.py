from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="classroom-home"),
    path('login', views.login, name="classroom-login"),
    path('createaccount', views.create_account, name="classroom-create-account"),
    path('myaccount', views.my_account, name="classroom-my-account"),
    path('performance-analysis', views.performance_analysis, name="classroom-performance-analysis"),
    path('select-language', views.select_language, name="classroom-select-language"),
    path('select-lesson', views.select_lesson, name="classroom-select-lesson"),
]
