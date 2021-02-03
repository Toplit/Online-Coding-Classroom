from django.shortcuts import render, redirect
from user.forms import AvgRegisterForm, AcademicRegisterForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse

@login_required
def home(request):
    """ View for mainsite homepage """
    context = {
        
    }
    return render(request, 'classroom_main/home.html', context)
    
def login(request):
    """ View for login path """
    context = {}
    return render(request, 'classroom_main/login.html', context)

def create_account(request, role):
    """ View for Create Account page """
    context = {}
    if request.method == "POST":
        if(role.lower() == "academic"):
            form = AcademicRegisterForm(request.POST)
        elif(role.lower() == "average"):
            form = AvgRegisterForm(request.POST)

        if(form.is_valid()):
            createNewUser(form)
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account has been created for {username}!")
            return redirect('login')
    else:
        if(role.lower() == "academic"):
            form = AcademicRegisterForm()
        elif(role.lower() == "average"):
            form = AvgRegisterForm()
        else:
            context['error'] = "URL does not exist. Please return to home and try again"
            return render(request, 'classroom_main/create_account.html', context)

    context["type"] = role
    context['title'] = "Sign up to the Online Coding Classroom"
    context['form'] = form

    return render(request, 'classroom_main/create_account.html', context)

@login_required
def my_account(request):
    """ View for My Account page """
    context = {}

    return render(request, 'classroom_main/my_account.html', context)

@login_required
def performance_analysis(request):
    """ View for Performance Analysis page page """
    context = {}

    return render(request, 'classroom_main/performance_analysis.html', context)

    
def createNewUser(form):
    email = form.cleaned_data.get('email')
    username = form.cleaned_data.get('username')
    role = form.cleaned_data.get('role')
    first_name = form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    password = form.cleaned_data.get('password1')

    get_user_model().objects.create_user(email, username, role, first_name, last_name, password)