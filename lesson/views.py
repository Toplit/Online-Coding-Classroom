import html
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from lesson.models import Lesson, ProgrammingEnvironment
from lesson import services

@login_required
def select_language(request, environmentName):
    """ View for Select Language page """
    context = {}
    lessonCount = {}
    languages = services.get_languages(environmentName)

    for language in languages:
        if(' ' in language.language_name):
            language.img_name = language.language_name.replace(" ","")
        lessonCount[language.language_name] =  services.get_lessons(language.language_name).count()

    context['languages'] = languages
    context['lessonCount'] = lessonCount

    return render(request, 'lesson/select_language.html', context)

@login_required
def select_env(request):
    """ View for Select Language page """
    context = {}
    languageCount = {}
    allEnvironments = ProgrammingEnvironment.objects.all()

    for env in allEnvironments:
        languageCount[env.environment_name] = services.get_languages(env.environment_name).count()

    context['environments'] = allEnvironments
    context['languageCount'] = languageCount

    return render(request, 'lesson/select_env.html', context)

@login_required
def select_lesson(request, languageTitle):
    """ View for Select Lesson page """
    context = {}
    languageLessons = services.get_lessons(languageTitle)
    context['lessons'] = languageLessons
    context['languageName'] = languageTitle

    return render(request, 'lesson/select_lesson.html', context)

@login_required
def lesson(request, languageTitle, lessonTitle):
    """ View for the lesson itself """
    context = {}
    selectedLesson = services.get_language_lesson(languageTitle, lessonTitle)
    lessonNum = selectedLesson[0].lesson_number
    lessonNum += 1
    nextLesson = Lesson.objects.filter(lesson_number__exact=lessonNum) ### CHANGE AS THIS TAKES ANY LESSON NUM

    context['lesson'] = selectedLesson[0]
    context['language'] = languageTitle.lower()
    try:
        context['nextLesson'] = nextLesson[0].lesson_title
    except IndexError:
        context['completed'] = True

    return render(request, 'lesson/lesson_base.html', context) 
    
def compile_code(request):
    """ Function for compiling code based on language"""
    language = request.GET.get('language')

    if(language == "javascript"):
        data = services.compile_javascript_code(request)
    elif(language == "python"):
        data = services.compile_python_code(request)
    elif(html.unescape(language) == "html and css"):
        data = services.compile_web_code(request)  
    return data

