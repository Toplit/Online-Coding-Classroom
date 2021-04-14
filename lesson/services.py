from django.template.defaulttags import register
from django.http import JsonResponse
import re
from node_vm2 import NodeVM
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import guarded_iter_unpack_sequence
from lesson.models import Lesson, Language, LessonHint
from classroom_main.models import Progress

### This Python module stores all functions used by views.py - Includes database calls and functions for code compilation


# Custom filter for accessing dictionaries from template
@register.filter
def get_value(dictionary, key):
    """ Registered filter used for getting values from a dictionary using a key | Used within Django templates """
    return dictionary.get(key)

def get_lessons(languageName):
    """ Function for getting lessons using language name """
    return Lesson.objects.filter(language__language_name__iexact=languageName)

def get_languages(envName):
    """ Function for getting languages using environment name """
    return Language.objects.filter(environment__environment_name__iexact=envName)

def get_lesson_progress(lessonTitle, languageTitle, username):
    """ Function for getting lesson progress """
    return Progress.objects.filter(lesson__lesson_title__iexact=lessonTitle).filter(lesson__language__language_name__iexact=languageTitle).filter(user__username__iexact=username)

def get_all_user_progress(username):
    return Progress.objects.filter(user__username__iexact=username)

def get_lesson_by_number(languageTitle, lessonNum):
    """ Function for getting a lesson using the language and lesson number """
    return Lesson.objects.filter(language__language_name__iexact=languageTitle).filter(lesson_number=lessonNum)

def get_all_languages():
    """ Function for getting all languages """
    return Language.objects.all()

def get_language_lesson(languageName, lessonTitle):
    """ Function for getting lesson using language name and lesson title """
    return Lesson.objects.filter(language__language_name__iexact=languageName).filter(lesson_title__iexact=lessonTitle)

def get_single_language(languageName):
    """ Function for getting a single language using language name """
    return Language.objects.filter(language_name__iexact=languageName)

def get_lesson_hint(lesson):
    return LessonHint.objects.filter(lesson=lesson)

def check_lesson_enabled(languageTitle, lessonTitle, username):
    """ Function for checking if the lesson can be accessed """
    enabled = True
    lesson = get_language_lesson(languageTitle, lessonTitle)
    
    if not lesson:
        enabled = False
    elif lesson[0].lesson_number == 1:
        enabled = True
    elif lesson[0].lesson_number > 1:
        lesson = get_lesson_by_number(languageTitle, lesson[0].lesson_number-1)[0]
        prevProgress = get_lesson_progress(lesson.lesson_title, languageTitle, username)

        if not prevProgress:
            enabled =  False
    else:
        enabled = False

    return enabled

def compile_web_code(request):
    """ Function to outputing HTML to view """
    untrustedCode = request.GET.get('untrustedCode') # Retrieve the user submitted code
    coreHTMLStruct = ["<html>", "</html>", "<body>", "</body>", "<head>", "</head>"] # List to store the core HTML structures
    message = ""
    # Check that the user input code containers the core HTML structure
    for text in coreHTMLStruct:
        if text not in untrustedCode:
            message = "You forgot to add core HTML structures such as <html>, <body> or <head>!"
            break
    data = {'HTML': untrustedCode,
            'output': message}
    # Return the code and error message to JavaScript for further validation
    return JsonResponse(data)

def compile_python_code(request):
    """ Function for compiling Python code """
    # Set global variables to allow safe for loop iteration
    glb = safe_globals.copy()
    glb['_getiter_'] = default_guarded_getiter
    glb['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
    # Get the submitted untrusted code
    untrustedCode = request.GET.get('untrustedCode')
    untrustedCode = untrustedCode.replace('\t', '    ')
    # Get the function name from untrusted code using regex
    lessonTitle = re.search('def (.*)():', untrustedCode)
    # Isolate the function name
    lessonTitle = lessonTitle.group(1).replace('(','').replace(')','')

    try:
        # loc used to store functions
        loc = {}
        # byteCode stores the restricted compilation configurations
        byteCode = compile_restricted(untrustedCode, '<inline>', 'exec')
        # Compile the untrusted code using restricted compilation configurations and store the function in loc
        exec(byteCode, glb, loc)

        # Retrieve the return from the user submitted function
        result = loc[lessonTitle]()
        data = {'output': result}
    # If a general SyntaxError is thrown
    except SyntaxError as e:
        data = {'output': "Error with the input code. Take another look at your code." + str(e)}
    # If a general Execption is thrown
    except Exception as e:
        # Check the user is not trying to use in-place operations
        if("+=" in untrustedCode):
            data = {'output': "Error with the input code. In-place operations ('+=') are not currently supported."}  
        else:
            data = {'output': "Error with the input code. Take another look at your code. \n" + str(e)}        
    return JsonResponse(data)

def compile_javascript_code(request):
    """ Function for compiling JavaScript code """
    # Get the submitted untrusted code
    untrustedCode = request.GET.get('untrustedCode')

    # Add the prefix to the user submitted code needed for NodeVM
    js = "exports.func = " + untrustedCode

    try:
        with NodeVM.code(js) as module:
            # Call the function described within js
            result = module.call_member("func") 
            
            data = {'output': result}
    except:
        data = {'output': "Error with the input code. Take another look at your code."}
    return JsonResponse(data)

### This function is not currently used, but has been developed ready for future lessons
def compile_array_code(request):
    """ Function for compiling code that returns an array """
    # Get the submitted untrusted code
    untrustedCode = request.GET.get('untrustedCode')

    # Add the prefix to the user submitted code needed for NodeVM
    js = "exports.func = " + untrustedCode

    with NodeVM.code(js) as module:
        # Call the function described within js
        result = module.call_member("func")

        # Convert the array into a String 
        stringResult = ' '.join(map(str, result))
        data = {'output': stringResult}
    return JsonResponse(data)