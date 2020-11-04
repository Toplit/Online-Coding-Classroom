from django.shortcuts import render
# from django.http import HttpResponse

def home(request):
    """ View for mainsite homepage """
    context = {}
    return render(request, 'classroom_main/home.html', context)
    
def login(request):
    """ View for login path """
    context = {}
    return render(request, 'classroom_main/login.html', context)

def create_account(request):
    """ View for Create Account page """
    context = {'title' : "Sign up to the Online Coding Classroom",}

    return render(request, 'classroom_main/create_account.html', context)

def my_account(request):
    """ View for My Account page """
    context = {}

    return render(request, 'classroom_main/my_account.html', context)

def performance_analysis(request):
    """ View for Performance Analysis page page """
    context = {}

    return render(request, 'classroom_main/performance_analysis.html', context)

def select_language(request):
    """ View for Select Language page page """
    context = {}

    return render(request, 'classroom_main/select_language.html', context)

def select_lesson(request):
    """ View for Select Lesson page page """
    context = {
        # title = selected language + " Lessons"
    }

    return render(request, 'classroom_main/select_lesson.html', context)
