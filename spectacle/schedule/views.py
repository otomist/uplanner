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
    highlight_schedule = True
    num_dept = 0
    num_key = 0
    
    if form.is_valid():
        # The user has entered some information to search for
        if not (form.cleaned_data['keywords'] == '' and form.cleaned_data['departments'] == 'NULL'):
            # The depatments dropdown has been used; return some subset from that dept
            if form.cleaned_data['departments'] != 'NULL':
                results = Course.objects.filter(dept__code=form.cleaned_data['departments'])
            if form.cleaned_data['keywords'] != '':
                keys = form.cleaned_data['keywords']
                # Return a subset from the selected dept
                if form.cleaned_data['departments'] != 'NULL':
                    dept_set = results
                    results = results.filter(title__icontains=keys)
                    results.union(results, dept_set.filter(description__icontains=keys))
                # Return a subset from all courses; no dept selected
                else:
                    results = Course.objects.filter(title__icontains=keys)
                    results.union(results, Course.objects.filter(description__icontains=keys))
        # Display error - no search parameters given
        else:
            pass
    
    # Display error - no search results match
    if len(results) == 0:
        pass
        
    # Todo: can there be too many results? (probably)
    
    # Reformat results to assign each course an index (for js button)
    results = list(zip(results, [x for x in range(1, len(results)+1)]))
    results = map(lambda r: {'id':r[1], 
                             'title':r[0].title, 
                             'dept':r[0].dept,
                             'number':r[0].number,
                             'description':r[0].description,
                             'reqs':r[0].reqs,
                             'lab': r[0].section_set.exclude(component='lec').exists(),
                             'open': r[0].section_set.filter(open=True).exists(),
                             'conflicts': False, #TODO: implement this
                             'credits': r[0].credits,
                             }, results)
    
    return render (
        request,
        'schedule.html',
        {'highlight_schedule':highlight_schedule, 'form':form, 'results':results}
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