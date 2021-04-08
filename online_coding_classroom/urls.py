"""online_coding_classroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classroom_main.urls')),   # Includes the URLS defined in classroom_main.urls
    path('', include('lesson.urls')),           # Includes the URLS defined in lesson.urls
    path('login/', auth_views.LoginView.as_view(template_name='classroom_main/login.html'), name="login"),    # Use the login.html as a LoginView class view 
    path('logout/', auth_views.LogoutView.as_view(template_name='classroom_main/logout.html'), name="logout"), # Use the logout.html as a LogoutView class view 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='classroom_main/password_reset.html'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='classroom_main/password_reset_done.html'), name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='classroom_main/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='classroom_main/password_reset_complete.html'), name="password_reset_complete"),
]
