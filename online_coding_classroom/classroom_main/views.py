from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    """ View for mainsite homepage """
    context = {
        
    }
    return render(request, 'classroom_main/home.html', context)
