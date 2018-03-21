from django.shortcuts import render
from django.views import generic
from .models import Course

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    
    return render(
        request,
        'index.html',
        context={}
    )
    
def schedule(request):
    
    return render(
        request,
        'schedule.html',
    )
    
class CourseDetailView(generic.DetailView):
    model = Course