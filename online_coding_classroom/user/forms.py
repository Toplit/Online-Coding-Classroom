from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

ROLE_CHOICES = (
    ('TEACHER', 'Teacher'),
    ('STUDENT', 'Student'),
)

TEMP_CHOICES = (
    ('AVERAGE', 'Average'),
)

class AvgRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    role = forms.ChoiceField(choices=TEMP_CHOICES)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']

class AcademicRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=30)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    is_staff = True

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role','password1', 'password2']