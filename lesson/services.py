from django.template.defaulttags import register
from django.http import JsonResponse
import re
# Import for Node_VM2
from node_vm2 import NodeVM
# Imports for RestrictedPython
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import guarded_iter_unpack_sequence

from lesson.models import Lesson, Language


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

def get_language_lesson(languageName, lessonTitle):
    """ Function for getting lesson using language name and lesson title """
    return Lesson.objects.filter(language__language_name__iexact=languageName).filter(lesson_title__iexact=lessonTitle)

def get_single_language(languageName):
    """ Function for getting a single language using language name """
    return Language.objects.filter(language_name__iexact=languageName)

def compile_web_code(request):
    """ Function to outputing HTML to view """
    untrustedCode = request.GET.get('untrustedCode')
    coreHTMLStruct = ["<html>", "</html>", "<body>", "</body>", "<head>", "</head>"]
    message = ""
    for text in coreHTMLStruct:
        if text not in untrustedCode:
            message = "You forgot to add core HTML structures such as <html>, <body> or <head>!"
            break
    data = {'HTML': untrustedCode,
            'output': message}
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

def compile_javascript_code(request):
    """ Function for compiling JavaScript code """

    untrustedCode = request.GET.get('untrustedCode')

    js = "exports.func = " + untrustedCode

    try:
        with NodeVM.code(js) as module:
            result = module.call_member("func") 
            
            data = {'output': result}
    except:
        data = {'output': "Error with the input code. Take another look at your code."}
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