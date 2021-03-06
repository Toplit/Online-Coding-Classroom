from django.shortcuts import render
from django.http import JsonResponse
import re

from node_vm2 import NodeVM

from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import guarded_iter_unpack_sequence

import html

from lesson.models import Lesson, Language, ProgrammingEnvironment
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
def select_language(request, environmentName):
    """ View for Select Language page """
    context = {}
    print(environmentName)
    languages = Language.objects.filter(environment__environment_name__iexact=environmentName)

    for language in languages:
        if(' ' in language.language_name):
            language.img_name = language.language_name.replace(" ","")

    context['languages'] = languages

    return render(request, 'lesson/select_language.html', context)

@login_required
def select_env(request):
    """ View for Select Language page """
    context = {}
    allEnvironments = ProgrammingEnvironment.objects.all()

    context['environments'] = allEnvironments

    return render(request, 'lesson/select_env.html', context)

@login_required
def select_lesson(request, languageTitle):
    """ View for Select Lesson page """
    context = {}
    languageLessons = Lesson.objects.filter(language__language_name__iexact=languageTitle)
    context['lessons'] = languageLessons
    context['languageName'] = languageTitle

    return render(request, 'lesson/select_lesson.html', context)

@login_required
def lesson(request, languageTitle, lessonTitle):
    """ View for the lesson itself """
    context = {}
    selectedLesson = Lesson.objects.filter(language__language_name__iexact=languageTitle).filter(lesson_title__iexact=lessonTitle)
    lessonNum = selectedLesson[0].lesson_number
    lessonNum += 1
    nextLesson = Lesson.objects.filter(lesson_number__exact=lessonNum)

    lang = Language.objects.filter(language_name__iexact=languageTitle)
    environment = lang[0].environment
    

    context['lesson'] = selectedLesson[0]
    context['language'] = languageTitle.lower()
    try:
        context['nextLesson'] = nextLesson[0].lesson_title
    except IndexError:
        context['completed'] = True


    # input_code = request.POST.get("editor_input")
    # print(input_code)
    # output_code = ""
    # Compile the inputCode
    # Store result in context

    return render(request, 'lesson/lesson_base.html', context) 
    

   
def compile_javascript_code(request):
    """ Function for compiling JavaScript code """

    untrustedCode = request.GET.get('untrustedCode')

    js = "exports.func = " + untrustedCode

    try:
        with NodeVM.code(js) as module:
            result = module.call_member("func") # Change to async | does not work in deployment
            
            data = {'output': result}
    except:
        data = {'output': "Error with the input code. Take another look at your code."}
    return JsonResponse(data)

def compile_code(request):
    """ Function for compiling code based on language"""
    language = request.GET.get('language')

    if(language == "javascript"):
        data = compile_javascript_code(request)
    elif(language == "python"):
        data = compile_python_code(request)
    elif(html.unescape(language) == "html and css"):
        data = compile_web_code(request)
    
    return data

def compile_python_code(request):
    """ Function for compiling Python code """
    # Set global variables to allow safe for loop iteration
    glb = safe_globals.copy()
    glb['_getiter_'] = default_guarded_getiter
    glb['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
    # Get the submitted untrusted code
    untrustedCode = request.GET.get('untrustedCode')
    untrustedCode = untrustedCode.replace('\t', '    ')
    # Get the function name from untrusted code - ### Can be changed to use actual lesson title from ajax call ###
    lessonTitle = re.search('def (.*)():', untrustedCode)
    lessonTitle = lessonTitle.group(1).replace('(','').replace(')','')

    try:
        loc = {}
        byteCode = compile_restricted(untrustedCode, '<inline>', 'exec')
        exec(byteCode, glb, loc)

        result = loc[lessonTitle]()
        data = {'output': result}
    except SyntaxError as e:
        data = {'output': "Error with the input code. Take another look at your code." + str(e)}
    except Exception as e:
        if("+=" in untrustedCode):
            data = {'output': "Error with the input code. In-place operations ('+=') are not currently supported."}  
        else:
            data = {'output': "Error with the input code. Take another look at your code. \n" + str(e)}        
    return JsonResponse(data)

def compile_web_code(request):
    """ Function to outputing HTML to view """
    data = {'output': request.GET.get('untrustedCode')}
    return JsonResponse(data)



def compile_array_code(request):
    """ Function for compiling code that returns an array """
    print("Compiling Code\n")

    untrustedCode = request.GET.get('untrustedCode')

    js = "exports.func = " + untrustedCode

    with NodeVM.code(js) as module:
        result = module.call_member("func")

        stringResult = ' '.join(map(str, result))
        data = {'output': result}
    return JsonResponse(data)