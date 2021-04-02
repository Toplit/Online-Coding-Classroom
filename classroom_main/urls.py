from django.urls import path
from django.conf.urls import url
from . import views

# All urls for Classroom_main
urlpatterns = [
    path('', views.home, name="classroom-home"),
    path('createaccount/<str:role>', views.create_account, name="classroom-create-account"),
    path('myaccount', views.my_account, name="classroom-my-account"),
    path('performance-analysis', views.performance_analysis, name="classroom-performance-analysis"),
]
