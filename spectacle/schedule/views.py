from itertools import chain

from django.shortcuts import render
from django.views import generic
from .models import Course, Department
from .forms import ScheduleForm

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
    """
    The view for the schedule uses a form with GET for receiving search parameters
    Eventually it will also have POST for updating the database when the user adds
    a course to their schedule
    """
    form = ScheduleForm(request.GET)
    results = []
    #departments = Department.objects.all()
    highlight_schedule = True
    num_dept = 0
    num_key = 0
    
    if form.is_valid():
        if not (form.cleaned_data['keywords'] == '' and form.cleaned_data['departments'] == 'NULL'):
            #form.cleaned_data['keywords'] = 'SUCCESS'
            #form.cleaned_data['departments'] = ''
            dept_set = []
            if form.cleaned_data['departments'] != 'NULL':
                dept_set = Course.objects.filter(dept__code=form.cleaned_data['departments'])
                num_dept = dept_set.count()
            if form.cleaned_data['keywords'] != '':
                keys = form.cleaned_data['keywords']
                if form.cleaned_data['departments'] != 'NULL':
                    key_set = dept_set.filter(title__icontains=keys)
                    key_set = set(chain(key_set, dept_set.filter(description__icontains=keys)))
                else:
                    key_set = Course.objects.filter(title__icontains=keys)
                    key_set = set(chain(key_set, Course.objects.filter(description__icontains=keys)))
                num_key = len(key_set)

        else:
            #results = []
            #form.cleaned_data['keywords'] = 'FAILURE'
            debug = 'failure'
    
    return render (
        request,
        'schedule.html',
        {'num_dept':num_dept, 'num_key':num_key, 'highlight_schedule':highlight_schedule, 'form':form, 'results':results}
    )
    
def profile(request):
    
    highlight_profile = True
    
    return render(
        request,
        'profile.html',
        context={'highlight_profile':highlight_profile}
    )
    
def prereqs(request):

    highlight_prereqs = True
    
    return render(
        request,
        'prereqs.html',
        context={'highlight_prereqs':highlight_prereqs}
    )
    
class CourseDetailView(generic.DetailView):
    model = Course