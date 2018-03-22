from django.shortcuts import render
from django.views import generic
from .models import Course, Department

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
    
    departments = Department.objects.all()
    
    return render(
        request,
        'schedule.html',
        context={'departments':departments}
    )
    
def userprofile(request):
    
    return render(
        request,
        'userprofile.html'
    )
    
def flowchart(request):
    
    return render(
        request,
        'flowchart.html'
    )
    
class CourseDetailView(generic.DetailView):
    model = Course