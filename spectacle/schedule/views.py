from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from .models import Course, Department, User, Section, Schedule, ScheduleCourse
from .forms import ScheduleForm
from .forms import flowchartForm
from django.contrib.auth.decorators import login_required
import json
import re

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
    
# ajax view
def del_section(request):
    """
    A non-rendering view that handles ajax requests for deleting
    a course from a js schedule. simply updates the database
    """
    id = request.GET.get('id', None)
    section = Section.objects.filter(id=id)[0]
    schedulecourse = ScheduleCourse.objects.filter(course=section)
    if schedulecourse.exists():
      schedulecourse[0].delete()
    
    data = {
        'success': True,
    }
    
    return JsonResponse(data)
    
# ajax view
def add_section(request):
    """
    The non-rendering "view" that handles ajax requests for adding a section to the
    js schedule
    """
    id = request.GET.get('id', None)
    schedule = request.GET.get('schedule', None)
    
    section = Section.objects.filter(id=id)[0]
    title = section.clss.dept.code + ' ' + section.clss.number
    start_time = section.start
    end_time = section.ending
    days = section.days
    
    if not schedule == None:
      schedule = Schedule.objects.filter(title=schedule)[0]
      if not ScheduleCourse.objects.filter(course=section).exists():
          ScheduleCourse.objects.create_schedulecourse(section, schedule)
      else:
          schedulecourse = ScheduleCourse.objects.filter(course=section)[0]
          schedulecourse.schedule = schedule
          schedulecourse.save()
    data = {
        'id': id,
        'start_time': start_time,
        'end_time': end_time,
        'title': title,
        'days': days,
    }
    
    return JsonResponse(data)
    
# returns data needed to fill in a course tab
def get_tab_data(course):
    
    components = map(
                 lambda comp: 
                        {'name': comp[1],
                         'sections':course.section_set.filter(component=comp[0])},
                        Section.COMPONENTS)

    return {
            'course':course,
            'sections':components,
            }
    
# renders a single tab's contents.
def make_tab_content(request):
    course_pk = request.GET.get('course_pk', None)
    
    course = Course.objects.filter(pk=course_pk)[0]
    
    return render (
        request,
        'schedule_tabs_content.html',
        get_tab_data(course)
    )

# returns data needed to render a single current course listing
def get_current_data(schedulecourse):
    section = schedulecourse.course
    course = section.clss
    return {
        'title': course.title,
        'number': course.number,
        'id': section.id,
    }
    

def make_current_courses(request):
    course_id = request.GET.get('course_id', None)
    section = Section.objects.filter(id=course_id)[0]
    schedulecourse = section.schedulecourse_set.all()[0]
    
    print(schedulecourse)
    
    return render (
        request,
        'schedule_current_courses.html',
        {'course':get_current_data(schedulecourse)}
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
    course_views = []
    user_courses = []
    user_schedules = []
    context = {}
    
    #replace with actual user later
    user = User.objects.all()[0]
    for schedule in user.schedule_set.all():
        user_schedules.append(schedule)
        for section in schedule.schedulecourse_set.all():
            user_courses.append(get_current_data(section))
            
    # these are the course tabs previously opened and stored in a session
    # note that each element of a course_tab must also agree with the format served by
    # make_tab_content()
    course_tabs = []
    for course in course_tabs:
        course_tabs.append(get_tab_data(course))
        
        
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
                             'geneds': list(map(lambda g: "{}({})".format(g.code, g.name), r[0].gened.all())),
                             'conflicts': False, #TODO: implement this
                             'credits': r[0].credits,
                             'pk': r[0].pk,
                             }, results)
            
    return render (
        request,
        'schedule.html',
        {'highlight_schedule':highlight_schedule, 'form':form, 'results':results, 'course_tabs':course_tabs, 'user_schedules':user_schedules, 'user_courses':user_courses}
    )


@login_required(login_url='/profile/login/')
def profile(request):
    
    highlight_profile = True
    
    # temporarily just grab the first user
    user = User.objects.all()[0]
    user_courses = map(lambda c: {
                                  'dept':c.clss.dept,
                                  'number':c.clss.number,
                                  'description':c.clss.description,
                                  'credits':c.clss.credits,
                                  }
                                  , user.courses.all())
    
    return render(
        request,
        'profile.html',
        context={'highlight_profile':highlight_profile, 'user':user, 'user_courses':user_courses}
    )
    
def prereqs(request):

    form = flowchartForm(request.GET)
    course_list = []

    highlight_prereqs = True
    
    #Populate the flowchart
    if form.is_valid(): 
        if(form.cleaned_data['departments'] != 'NULL'):
            course_list = Course.objects.filter(dept__code=form.cleaned_data['departments'])

    #this is a very silly way to tranfser the data but it works for now until I start using ajax.
    course_list = json.dumps(list(map(lambda c: {str(c.number):[
                                 c.reqs.split(" "),
                                 len(c.reqs.split(" ")),
                                 c.title,
                                 c.description]
        }, list(course_list))))
    
    #DEBUG:
    #print("\nlist: ", course_list,"\n")
    # print(type(course_list))
    # for x in course_list:
    #     print("\nDEBUG:: ", x['title'], '\n')

    return render(
        request,
        'prereqs.html',
        context={'highlight_prereqs':highlight_prereqs, 'form':form, 'course_list':course_list}
    )
    
class CourseDetailView(generic.DetailView):
    model = Course