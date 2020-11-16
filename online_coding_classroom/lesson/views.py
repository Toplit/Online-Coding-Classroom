from django.shortcuts import render


def select_language(request):
    """ View for Select Language page page """
    context = {}

    return render(request, 'lesson/select_language.html', context)

def select_lesson(request):
    """ View for Select Lesson page page """
    context = {
        # title = selected language + " Lessons"
    }

    return render(request, 'lesson/select_lesson.html', context)