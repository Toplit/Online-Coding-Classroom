import html
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from lesson.models import Lesson, ProgrammingEnvironment
from lesson import services

# @login_required decorator used on views that should not be accessed without being logged in

@login_required
def select_language(request, environmentName):
    """ View for Select Language page """
    context = {}
    lessonCount = {}
    languages = services.get_languages(environmentName)

    # Modify data from languages for context
    for language in languages:
        if(' ' in language.language_name):
            # Remove spaces in the language name and store it as img_name - This is used as the name for language icons in the view
            language.img_name = language.language_name.replace(" ","")
        # Store the number of lessons the current language has
        lessonCount[language.language_name] =  services.get_lessons(language.language_name).count()

    context['languages'] = languages
    context['lessonCount'] = lessonCount

    return render(request, 'lesson/select_language.html', context)

@login_required
def select_env(request):
    """ View for Select Language page """
    context = {}
    languageCount = {}
    # Retrieve all environments
    allEnvironments = ProgrammingEnvironment.objects.all()

    # Store the number of languages per environment in languageCount
    for env in allEnvironments:
        languageCount[env.environment_name] = services.get_languages(env.environment_name).count()

    context['environments'] = allEnvironments
    context['languageCount'] = languageCount

    return render(request, 'lesson/select_env.html', context)

@login_required
def select_lesson(request, languageTitle):
    """ View for Select Lesson page """
    context = {}
    # Retrieve all lessons for a specific language
    languageLessons = services.get_lessons(languageTitle)
    context['lessons'] = languageLessons
    context['languageName'] = languageTitle

    return render(request, 'lesson/select_lesson.html', context)

@login_required
def lesson(request, languageTitle, lessonTitle):
    """ View for the lesson itself """
    context = {}
    # Get the selected lesson data
    selectedLesson = services.get_language_lesson(languageTitle, lessonTitle)
    # Retrieve the lesson number 
    lessonNum = selectedLesson[0].lesson_number
    # Increment the number by one and use this to retrieve the next lesson
    lessonNum += 1
    nextLesson = Lesson.objects.filter(lesson_number__exact=lessonNum) 

    context['lesson'] = selectedLesson[0]
    context['language'] = languageTitle.lower()
    # If there is not a next lesson, pass a 'completed' variable to the view instead
    try:
        context['nextLesson'] = nextLesson[0].lesson_title
    except IndexError:
        context['completed'] = True

    return render(request, 'lesson/lesson_base.html', context) 

def language_complete(request, languageTitle):
    context = {}
    context['language'] = services.get_single_language(languageTitle)[0]
    print(context['language'])
    return render (request, 'lesson/language_complete.html', context)
    
def compile_code(request):
    """ Function for compiling code based on language"""
    # Retrieve the language from the request
    language = request.GET.get('language')

    # Execute the relavant function for the language
    if(language == "javascript"):
        data = services.compile_javascript_code(request)
    elif(language == "python"):
        data = services.compile_python_code(request)
    elif(html.unescape(language) == "html and css"):
        data = services.compile_web_code(request)  
    return data

