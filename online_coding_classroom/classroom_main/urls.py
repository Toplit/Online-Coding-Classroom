from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="classroom-home"),
    path('createaccount', views.create_account, name="classroom-create-account"),
]
