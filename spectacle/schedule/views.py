from django.shortcuts import render
from django.views import generic
from .models import Course, Department

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    highlight_index = True
    
    return render(
        request,
        'index.html',
        context={'highlight_index':highlight_index}
    )
    
def schedule(request):
    
    departments = Department.objects.all()
    highlight_schedule = True
    
    return render(
        request,
        'schedule.html',
        context={'departments':departments, 'highlight_schedule':highlight_schedule}
    )
    
def profile(request):
    
    highlight_profile = True
    
    return render(
        request,
        'userprofile.html',
        context={'highlight_profile':highlight_profile}
    )
    
def prereqs(request):

    highlight_prereqs = True
    
    return render(
        request,
        'flowchart.html',
        context={'highlight_prereqs':highlight_prereqs}
    )
    
class CourseDetailView(generic.DetailView):
    model = Course