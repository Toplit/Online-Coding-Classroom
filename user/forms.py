from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from classroom_main.models import ComputingClass, School

# Choices specified below for academic and average roles
ROLE_CHOICES = (
    ('TEACHER', 'Teacher'),
    ('STUDENT', 'Student'),
)

TEMP_CHOICES = (
    ('AVERAGE', 'Average'),
)

# Form for average users
class AvgRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

# Form for academic users - The class and school is specified after account creation
class AcademicRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=30)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    #is_staff = True

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role','password1', 'password2']

class PasswordResetForm(forms.Form):
    old_password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type':'password',
                                                                                'placeholder':'Enter your old password'}))
    new_password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type':'password',
                                                                                'placeholder':'Enter your new password'}))               
    confirm_password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type':'password',
                                                                                'placeholder':'Confirm your new password'}))                                         

    def clean(self):
        if 'new_password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
                raise forms.ValidationError("The passwords you have entered do not match")
        return self.cleaned_data