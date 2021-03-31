from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from classroom_main import services
from user.forms import AvgRegisterForm, AcademicRegisterForm

# @login_required decorator used on views that should not be accessed without being logged in

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
        # Use a different form depending on the Role type
        if(role.lower() == "academic"):
            #form = AcademicRegisterForm(request.POST)
            context['error'] = "Academic accounts not yet implemented. Please return to home and create a normal account."
            return render(request, 'classroom_main/create_account.html', context)
        elif(role.lower() == "average"):
            form = AvgRegisterForm(request.POST)

        # Check the form is valid
        if(form.is_valid()):
            if(role.lower() == "average"):
                services.createNewUser(form)
                username = form.cleaned_data.get('username')
                messages.success(request, f"Account has been created for {username}!")
                return redirect('login')
            elif(role.lower() == "academic"):
                services.createNewAcademicUser(form)
                username = form.cleaned_data.get('username')
                messages.success(request, f"Account has been created for {username}!")
                return redirect('login')
    else:
        # Use a different form depending on the Role type
        if(role.lower() == "academic"):
            #form = AcademicRegisterForm()
            context['error'] = "Academic accounts not yet implemented. Please return to home and create a normal account."
            return render(request, 'classroom_main/create_account.html', context)
        elif(role.lower() == "average"):
            form = AvgRegisterForm()
        else:
            context['error'] = "URL does not exist. Please return to home and try again"
            return render(request, 'classroom_main/create_account.html', context)

    # Organise context to be used by the view
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