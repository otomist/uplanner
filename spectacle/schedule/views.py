from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.urls import reverse
from .models import Course, Department, Student, Section, Schedule, ScheduleCourse
from .forms import ScheduleForm, NewScheduleForm, flowchartForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from schedule.forms import userRegistration
import json
import re

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
    
#==================================================================#    
#       v-------------Start schedule views------------v
#==================================================================#

# ajax view
def schedule_courses(request):
    """
    An ajax view ran every time the schedule page is loaded.
    it passes json with the current courses on the schedule to scheduleBuilder.js
    for rendering
    """
    schedule_title = request.GET.get('schedule', None)
    
    temp_courses = ScheduleCourse.objects.all()
    courses = []
    
    def parse_dates(dates):
        days = []
        for i in range(0, len(dates), 2):
            day = dates[i:i+2]
            if day == "Mo":
                days.append('2018-01-01')
            if day == "Tu":
                days.append('2018-01-02')
            if day == "We":
                days.append('2018-01-03')
            if day == "Th":
                days.append('2018-01-04')
            if day == "Fr":
                days.append('2018-01-05')
        return days
    
    for scourse in temp_courses:
        course = scourse.course
        i = 0
        for date in parse_dates(course.days):
            courses.append({
                'id': "{}{}{}".format(course.id, i, scourse.schedule.title),
                'start_date': date + " " + str(course.start),
                'end_date': date + " " + str(course.ending),
                'text': "{} {}".format(course.clss.dept.code, course.clss.number),
                'type': scourse.schedule.title,
                'color': '#157ddf9f',
                'readonly': True,
            })
            i += 1
            
    schedule = schedule_title
    if 'active_schedule' in request.session:
        schedule = request.session['active_schedule']
    else:
        request.session['active_schedule'] = schedule
        request.session.save()
        
    print("active schedule is ", schedule)
        
    data = {
        'count': len(courses),
        'courses': courses,
        'active_schedule': schedule,
        'url': reverse(make_current_courses),
    }
    
    return JsonResponse(data)
    
# ajax view
def del_section(request):
    """
    A non-rendering view that handles ajax requests for deleting
    a course from a js schedule. simply updates the database
    """
    id = request.GET.get('id', None)
    schedule_title = request.GET.get('schedule', None)
    
    # TODO: this will break if the section/schedule are not found
    section = Section.objects.filter(id=id)[0]
    schedule = Schedule.objects.filter(title=schedule_title)[0]
    
    schedulecourse = ScheduleCourse.objects.filter(course=section).filter(schedule=schedule)
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
    schedule_id = Schedule.objects.filter(title=schedule)[0].id
    
    if not schedule == None:
        # TODO: this will break if the schedule doesn't exist
        schedule = Schedule.objects.filter(id=schedule_id)[0]
        if not ScheduleCourse.objects.filter(course=section).filter(schedule=schedule).exists():
            ScheduleCourse.objects.create_schedulecourse(section, schedule)

    data = {
        'id': id,
        'start_time': start_time,
        'end_time': end_time,
        'title': title,
        'days': days,
        'schedule_id':schedule_id,
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
    
    #TODO: this will break if size of list is 0
    course = Course.objects.filter(pk=course_pk)[0]
    print("Add a new tab to session!")
    print("Course is ", course_pk)
    if 'tabs' in request.session:
        request.session['tabs'].append(course_pk)
        request.session.save()
    else:
        request.session['tabs'] = [course_pk]
        request.session.save()
        
    return render (
        request,
        'schedule_tabs_content.html',
        {'tab':get_tab_data(course)}
    )
    
def delete_tab(request):
    course_pk = request.GET.get('id', None)
    #TODO: this will fail if course doesn't exist
    course = Course.objects.filter(pk=course_pk)[0]
    if 'tabs' in request.session:
        if course_pk in request.session['tabs']:
            request.session['tabs'].remove(course_pk)
            request.session.save()

    return JsonResponse({'status':'SUCCESS'})

# returns data needed to render a single current course listing
def get_current_data(schedulecourse):
    section = schedulecourse.course
    course = section.clss
    return {
        'title': course.title,
        'number': course.number,
        'id': section.id,
        'professor': section.professor,
    }

def make_current_course(request):
    course_id = request.GET.get('course_id', None)
    schedule_id = request.GET.get('schedule', None)
    
    # TODO: this will break if any of these do not exist
    section = Section.objects.filter(id=course_id)[0]
    #schedulecourse = section.schedulecourse_set.all()[0]
    schedule = Schedule.objects.filter(id=schedule_id)[0]
    schedulecourse = section.schedulecourse_set.filter(schedule=schedule)[0]
    
    return render (
        request,
        'schedule_current_course.html',
        {'course':get_current_data(schedulecourse)}
    )
    
def make_current_courses(request):
    schedule_id = request.GET.get('schedule', None)
    
    schedule = Schedule.objects.filter(id=schedule_id)[0]
    
    user_courses = []
    
    for course in schedule.schedulecourse_set.all():
        user_courses.append(get_current_data(course))
        
    return render (
        request,
        'schedule_current_courses.html',
        {'user_courses':user_courses,}
    )

def del_schedule(request):
    schedule_title = request.GET.get('schedule', None)
    new_schedule_title = request.GET.get('new_schedule', None)
    schedule = Schedule.objects.filter(title=schedule_title)
    if schedule.exists():
        schedule[0].delete()
    request.session['active_schedule'] = new_schedule_title
    return JsonResponse({})
    
# ajax view for making a new schedule
# TODO: currently, form.is_valid() does not get triggered without
# page reload. Consider bypassing forms altogether
def make_schedule(request):
    if request.is_ajax():
        form = NewScheduleForm(request.POST)
        data = {'status':'failure'}
        if form.is_valid():
            title = form.cleaned_data['title']
            
            data['title'] = title
            data['url'] = reverse(make_current_courses)
            data['schedule_url'] = reverse(change_schedule)
            if not Schedule.objects.filter(title=title):
                Schedule.objects.create_schedule(title, Student.objects.all()[0])
            data['id'] = Schedule.objects.filter(title=title)[0].id
            
        else:
            # check why title is invalid??
            pass
            
        return JsonResponse(data)
    else:
        # THIS SHOULD NEVER HAPPEN - this is an ajax view, and shouldn't render anything
        print("=============Error! new schedule form received non-ajax request!============")
        return schedule(request) # attempt to salvage situation
    
# ajax view for updating session when schedule is changed
def change_schedule(request):
    print("got a request!")
    active_schedule = request.GET.get('schedule_title')
    request.session['active_schedule'] = active_schedule
    request.session.save()
    return JsonResponse({'status':'SUCCESS'})
    
def schedule(request):
    """
    The view for the schedule uses a form with GET for receiving search parameters
    Eventually it will also have POST for updating the database when the user adds
    a course to their schedule
    """
    form = ScheduleForm(request.GET)
    schedule_form = NewScheduleForm(request.GET)
    results = []
    highlight_schedule = True
    num_dept = 0
    num_key = 0
    course_views = []
    user_courses = []
    user_schedules = []
    context = {}
    
    #replace with actual student later
    student = Student.objects.all()[0]
    for schedule in student.schedule_set.all():
        user_schedules.append(schedule)
    #as default, always displays the first schedule
    for section in student.schedule_set.all()[0].schedulecourse_set.all():
        user_courses.append(get_current_data(section))
        
    # these are the course tabs previously opened and stored in a session
    # note that each element of a course_tab must also agree with the format served by
    # make_tab_content()
    course_tabs = []
    if 'tabs' in request.session:
        tabs = request.session['tabs']
        for course_pk in tabs:
            #TODO: this will fail if course doesn't exist
            course = Course.objects.filter(pk=course_pk)[0]
            data = get_tab_data(course)
            course_tabs.append(get_tab_data(course))
        
        
    if form.is_valid():
        
        results = Course.objects.all()
        
        #filter based on department
        if form.cleaned_data['departments'] != 'NULL':
            results = results.filter(dept__code=form.cleaned_data['departments'])
        
        #filter based on keywords
        if form.cleaned_data['keywords'] != '':
            keys = form.cleaned_data['keywords']
            title_set = results.filter(title__icontains=keys)
            desc_set = results.filter(description__icontains=keys)
            results = title_set.union(desc_set)
        
        #filter based on days
        #if a course has at least one related section with days
        #  containing day, keep it in the results.
        days_set = None
        for day in form.get_days():
            if form.cleaned_data[day]:
                if days_set == None:
                    days_set = results.select_related().filter(section__days__contains=day[:2]).distinct()
                else:
                    days_set.union(results.select_related().filter(section__days__contains=day[:2]).distinct())
        if days_set != None:
            results = days_set
        
        #if department/keywords are not selected, return nothing
        if form.cleaned_data['departments'] == 'NULL' and form.cleaned_data['keywords'] == '':
            results = []
    
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
        {'highlight_schedule':highlight_schedule, 'form':form, 'schedule_form':schedule_form, 'results':results, 'course_tabs':course_tabs, 'user_schedules':user_schedules, 'user_courses':user_courses}
    )

#==================================================================#    
#       ^-------------End schedule views------------^
#==================================================================#

from django.shortcuts import render, HttpResponse, redirect

@login_required(login_url='/profile/login/')
def profile(request):
    
    highlight_profile = True
    
    # temporarily just grab the first user
    student = Student.objects.all()[0]
    
    user_courses = map(lambda c: {
                                  'dept':c.clss.dept,
                                  'number':c.clss.number,
                                  'description':c.clss.description,
                                  'credits':c.clss.credits,
                                  }
                                  , student.courses.all())
    
    return render(
        request,
        'profile.html',
        context={'highlight_profile':highlight_profile, 'user':student, 'user_courses':user_courses}
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
from django.urls import reverse_lazy
class register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'
    '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('uplanner/schedule.html')

    else:
        form = UserCreationForm()
        args = {'form':form}
    return render(request, 'registration/registration_form.html', args)
'''
'''
def register(UserCreationForm):
    email = forms.EmailField(label="Email")
    fullname = forms.CharField(label="First Name")
    class Meta:
        model = User
        fields = ("username", "fullname", "email",)
    def save(self, commit=True):
        user=super(RegisterForm, self).save(commit=False)
'''
class CourseDetailView(generic.DetailView):
    model = Course