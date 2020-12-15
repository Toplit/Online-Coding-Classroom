from django.shortcuts import render
from django.http import JsonResponse


def select_language(request):
    """ View for Select Language page """
    context = {}

    return render(request, 'lesson/select_language.html', context)

def select_lesson(request):
    """ View for Select Lesson page """
    context = {
        # title = selected language + " Lessons"
    }

    return render(request, 'lesson/select_lesson.html', context)

def lesson(request):
    """ View for the lesson itself """



    # input_code = request.POST.get("editor_input")
    # print(input_code)
    # output_code = ""
    # Compile the inputCode
    # Store result in context
    context = {}
    return render(request, 'lesson/lesson_base.html', context)
    
def compile_code(request):
    print("Working")
    untrustedCode = request.GET.get('untrustedCode')
    data = {'response': f'Input code is: {untrustedCode}'}
    return JsonResponse(data)