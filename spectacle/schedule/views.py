from .models import Course, Department, Student, Section, Schedule, ScheduleCourse, Term
from .forms import ScheduleForm, NewScheduleForm, flowchartForm, StudentForm, UserForm, UserEventForm
from django.db import models
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse, QueryDict
from django.urls import reverse
from django.db.models import Q
import json
import re
import pickle

"""
TODO: 
 >rewrite fake json
"""


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
#   v------------------Start schedule views------------------v
#       contact jason.valladares3@gmail.com for questions
#==================================================================#

def get_schedulecourse_data(schedulecourse):
    """
    Given a schedulecourse, get the data needed to add it to the javascript schedule
    """
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
    
    courses = []
    course = schedulecourse.course
    i = 0
    for date in parse_dates(course.days):
        d = {
            'id': "{}{}{}".format(course.uid, i, schedulecourse.schedule.title),
            'start_date': date + " " + str(course.start),
            'end_date': date + " " + str(course.ending),
            'type': schedulecourse.schedule.title,
            'color': schedulecourse.color,
            'readonly': True,
        }
        if course.component == "CUS":
            d['text'] = schedulecourse.title
        else:
            d['text'] = "{} {}".format(course.clss.dept.code, course.clss.number)
        courses.append(d)
        i += 1
    
    return courses
    

def schedule_courses(request):
    """
    An ajax view ran every time the schedule page is loaded.
    it passes json with the current courses on the schedule to scheduleBuilder.js
    for rendering
    This is the main function for initializing the schedule.
    """
    
    #TODO: this will fail if user does not exist
    current_user = Student.objects.filter(user_email=request.user.email)
    temp_courses = []
    if current_user.exists():
        temp_courses = ScheduleCourse.objects.filter(schedule__student=current_user[0])
    
    courses = []

    for scourse in temp_courses:
        courses += get_schedulecourse_data(scourse)

    schedule = ''
    if 'active_schedule' in request.session:
        schedule = request.session['active_schedule']
    elif current_user.exists():                         #then just fetch a random schedule
        #TODO: this breaks if doesn't exist
        schedule = Schedule.objects.filter(student=current_user[0])[0].title
        request.session['active_schedule'] = schedule
        request.session.save()
    
    #filters_expanded is handled here and in the main schedule view. here it just tells javascript
    # to flip the button
    filters_expanded = True
    if 'filters_expanded' in request.session:
        filters_expanded = request.session['filters_expanded']
    else:
        request.session['filters_expanded'] = filters_expanded
        request.session.save()
    
    data = {
        'count': len(courses),
        'courses': courses,
        'active_schedule': schedule,
        'filters_expanded': filters_expanded,
    }
    
    return JsonResponse(data)
    
    
def change_schedulecourse_color(request):
    """
    ajax view for changing a schedulecourse's color
    """
    
    id = request.GET.get('id')
    color = request.GET.get('color')
        
    schedule_title = request.session['active_schedule']
    
    current_user = Student.objects.get(user_email=request.user.email)
    # TODO: this will break if the section/schedule are not found
    schedule = Schedule.objects.get(title=schedule_title, student=current_user)
    section = Section.objects.get(uid=id)
    schedulecourse = ScheduleCourse.objects.get(schedule=schedule, course=section)
    schedulecourse.color = color
    schedulecourse.save()
    
    return JsonResponse({})
    
def update_session(request):
    """
    ajax view for updating the session variable
    """
    for k, v in request.GET.items():
        request.session[k] = v
    request.session.save()
    return JsonResponse({})
    

def del_section(request):
    """
    A non-rendering view that handles ajax requests for deleting
    a course from a js schedule. simply updates the database
    """
    id = request.GET.get('id', None)
    schedule_title = request.session['active_schedule']
    
    current_user = Student.objects.get(user_email=request.user.email)
    # TODO: this will break if the section/schedule are not found
    section = Section.objects.get(uid=id)
    schedule = Schedule.objects.get(title=schedule_title, student=current_user)
    
    schedulecourse = ScheduleCourse.objects.filter(course=section).filter(schedule=schedule)
    if schedulecourse.exists():
        schedulecourse[0].delete()
    
    data = {
        'success': True,
    }
    
    return JsonResponse(data)
    
    
def add_section(request):
    """
    The non-rendering "view" that handles ajax requests for adding a section to the
    js schedule
    """
    id = request.GET.get('id', None)
    #TODO: this will break if does not exist
    section = Section.objects.get(uid=id)
    current_user = Student.objects.get(user_email=request.user.email)
    
    color = None
    schedule = None
    if 'schedule' in request.GET:
        schedule = Schedule.objects.filter(student=current_user).get(title=request.GET.get('schedule', None))
        color = ScheduleCourse.objects.filter(schedule__title=request.session['active_schedule']).get(course=section).color
    else:
        schedule = Schedule.objects.filter(student=current_user).get(title=request.session['active_schedule'])

    if not ScheduleCourse.objects.filter(course=section).filter(schedule=schedule).exists():
        ScheduleCourse.objects.create_schedulecourse(section, schedule)
            
    schedulecourse = ScheduleCourse.objects.filter(course=section).get(schedule=schedule)
    
    if color != None:
        schedulecourse.color = color
        schedulecourse.save()
    
    data = {'events':get_schedulecourse_data(schedulecourse)}
    
    return JsonResponse(data)


def make_model_dict(model, extra_fields):
    """
    convenience function for model -> dict, so that the dictionary can be extended with extra_fieldss
    """
    d = {}
    for field in model._meta.get_fields():
        if not isinstance(field, models.ManyToManyRel) and not isinstance(field, models.ManyToOneRel):
            d[field.name] = eval('model.' + field.name)
    
    for item in extra_fields:
        d[item[0]] = item[1]
    return d
    
    
def get_conflicting_sections(section, request):
    """
    convenience function for returning a list of conflicts  with a given section. empty list if none
    """
    #TODO: breaks if 'active_schedule' not in request, or user is not logged in
    current_user = Student.objects.get(user_email=request.user.email)
    schedule = Schedule.objects.get(student=current_user, title=request.session['active_schedule'])
    
    current_courses = ScheduleCourse.objects.filter(schedule=schedule)
    # for every course in results, display it if:
    #   it has at least one section with a time/day that does not conflict with any
    #   of the courses in current_courses
    
    conflicts = current_courses.values_list('course__days', 'course__start', 'course__ending', 'course__uid').distinct()
    
    days = []
    for day_set, start, end, id in conflicts:
        for i in range(0, len(day_set), 2):
            days.append((day_set[i:i+2], start, end, id))
    
    # A list of tuples which current courses can't conflict with [(day, start, end), ...]
    conflicts = days
    
    conflict_courses = []
    for day, start, end, course_uid in conflicts:
        if day in section.days:
            if not (section.start > end or section.ending < start):
                conflict_courses.append(Section.objects.get(uid=course_uid))
    
    return conflict_courses
    
def section_in_schedule(section, request):
    current_user = current_user = Student.objects.get(user_email=request.user.email)
    schedule = Schedule.objects.filter(student=current_user).get(title=request.session['active_schedule'])
    return ScheduleCourse.objects.filter(schedule=schedule, course=section).exists()
    
def get_section_list(sections, request):
    """
    returns a dictionary per section where each dictionary also stores associated conflicts for that section
    """
    if sections.exists():
        return map(lambda section: make_model_dict(section, [('is_added', section_in_schedule(section, request)), ('conflicts', get_conflicting_sections(section, request))]), sections)
    else:
        return []
    
    
def get_tab_data(course, request=None):
    """
    returns data needed to fill in a course tab
    """
    components = []
    for comp in Section.COMPONENTS:
        sections = course.section_set.filter(component=comp[0])
        count = sections.count()
        sections = get_section_list(sections, request)
        comp_dict = {'name': comp[1],
                     'count': count,
                     'sections': sections,
                    }
        components.append(comp_dict)
    
    desc_overflow = False
    req_overflow = False
    
    #indicates that the description will overflow, and should be partially hidden
    if len(course.description) > 250:
        desc_overflow = True

    if len(course.reqs) > 250:
        req_overflow = True
    
    return {
            'course':course,
            'sections':components,
            'desc_overflow':desc_overflow,
            'req_overflow':req_overflow,
            }
    

def make_tab_content(request):
    """
    renders a single tab's contents. uses get_tab_data
    """
    course_pk = request.GET.get('course_pk', None)
        
    #TODO: this will break if course does not exist
    course = Course.objects.get(pk=course_pk)
    if 'tabs' in request.session:
        if course_pk not in request.session['tabs']:
            request.session['tabs'].append(course_pk)
            request.session.save()
    else:
        request.session['tabs'] = [course_pk]
        request.session.save()
        
    return render (
        request,
        'schedule_tabs_content.html',
        {'tab':get_tab_data(course, request)}
    )
    
    
def delete_tab(request):
    """
    deletes a tab, removing it from the sessions variable
    """
    course_pk = request.GET.get('id', None)
    #TODO: this will fail if course doesn't exist
    course = Course.objects.filter(pk=course_pk)[0]
    if 'tabs' in request.session:
        if course_pk in request.session['tabs']:
            request.session['tabs'].remove(course_pk)
            request.session.save()

    return JsonResponse({'status':'SUCCESS'})

    
def get_current_data(schedulecourse, request):
    """
    returns data needed to render a single "current course" listing
    """
    section = schedulecourse.course
    course = section.clss
    
    #if component is "CUS", it is a user-added event with no associated class
    if section.component=='CUS':
        title = "User event: " + schedulecourse.title
    else:
        title = course.dept.code + " " + course.number + " - " + course.title + " (" + section.component + ")"
    
    current_user = Student.objects.get(user_email=request.user.email)
    # each current course also has a listing of schedules it *doesn't* appear on
    schedules = Schedule.objects.filter(student=current_user).select_related().exclude(schedulecourse__course=section)
    
    colors = [color[0] for color in ScheduleCourse.COLORS]
    
    course_data = make_model_dict(section, [('title', title), ('schedules', schedules), ('colors', colors)])
        
    return course_data

    
def make_current_course(request):
    """
    renders a single element of "current courses". uses get_current_data
    """
    course_id = request.GET.get('course_id', None)
    schedule_title = request.session['active_schedule']
    
    current_user = Student.objects.get(user_email=request.user.email)
    schedule = Schedule.objects.filter(student=current_user).get(title=schedule_title)
    
    section = Section.objects.filter(uid=course_id)[0]
    
    schedulecourse = section.schedulecourse_set.get(schedule=schedule)
    
    return render (
        request,
        'schedule_current_course.html',
        {'course':get_current_data(schedulecourse, request)}
    )

def make_current_courses(request):
    """
    renders all elements of "current courses". uses get_current_data
    """
    schedule_title = request.session['active_schedule']
    current_user = Student.objects.get(user_email=request.user.email)
    schedule = Schedule.objects.filter(student=current_user).get(title=schedule_title)
    
    user_courses = []
    
    for course in schedule.schedulecourse_set.all():
        user_courses.append(get_current_data(course, request))
    
    return render (
        request,
        'schedule_current_courses.html',
        {'user_courses':user_courses,}
    )

def make_user_event(request):
    """
    ajax post form for creating a new user event and adding it to the schedule
    """
    if request.is_ajax():
        form = UserEventForm(request.POST)
        data = {'status':'FAILURE'}
        if form.is_valid():
            
            title = form.cleaned_data['title']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            days = form.cleaned_data['days']

            user_event_course = Section.objects.create_userevent(start_time=start_time, end_time=end_time, days=days)
            
            current_user = Student.objects.get(user_email=request.user.email)
            schedule = Schedule.objects.filter(student=current_user).get(title=request.session['active_schedule'])
            user_event = ScheduleCourse.objects.create_schedulecourse(course=user_event_course, schedule=schedule)
            user_event.title = title
            user_event.save()
            
            data['events'] = get_schedulecourse_data(user_event)
            
            data['status'] = 'SUCCESS'
            
        return JsonResponse(data)
    else:
        # THIS SHOULD NEVER HAPPEN - this is an ajax view, and shouldn't render anything
        print("=============Error! new schedule form received non-ajax request!============")
        return schedule(request) # attempt to salvage situation
    
    
def del_schedule(request):
    """
    Deletes a schedule
    """
    schedule_title = request.session['active_schedule']
    
    #TODO: this will break if user doesn't exist
    current_user = Student.objects.get(user_email=request.user.email)
    schedule = Schedule.objects.filter(student=current_user).get(title=schedule_title)
    # using list() should normally be avoided on a queryset, but it is reasonable to assume
    # that the course_ids set will be very small
    course_ids = []
    if schedule.schedulecourse_set.exists():
        course_ids = list(schedule.schedulecourse_set.values_list('course__uid', flat=True))
    schedule.delete()
    
    new_schedule_title = Schedule.objects.all()[0].title
    request.session['active_schedule'] = new_schedule_title
    request.session.save()
    
    return JsonResponse({'course_ids':course_ids, 'new_schedule_title':new_schedule_title})
    
# ajax view for making a new schedule
def make_schedule(request):
    """
    ajax view post form for making a new schedule
    """
    if request.is_ajax():
        form = NewScheduleForm(request.POST)
        data = {'status':'failure'}
        if form.is_valid():
            title = form.cleaned_data['title']
            current_user = Student.objects.get(user_email=request.user.email)
            data['title'] = title
            if not Schedule.objects.filter(student=current_user).filter(title=title):
                data['status'] = 'SUCCESS'
                Schedule.objects.create_schedule(title, current_user)

        return JsonResponse(data)
    else:
        # THIS SHOULD NEVER HAPPEN - this is an ajax view, and shouldn't render anything
        print("=============Error! new schedule form received non-ajax request!============")
        return schedule(request) # attempt to salvage situation
    
def change_schedule(request):
    """
    ajax view for updating session when schedule is changed
    """
    active_schedule = request.GET.get('schedule_title')
    request.session['active_schedule'] = active_schedule
    request.session.save()
    return JsonResponse({'status':'SUCCESS'})

@login_required(login_url='/profile/login/')
def schedule(request):
    """
    The view for the schedule uses a form with GET for receiving search parameters
    It handles rendering the entire page in accordance with all sub-rendering functions
    """
    form = None
    
    #If GET is not empty (ie, if the user has searched for something), use those search parameters to
    # populate form and get search results
    #If they have not, then populate search form based on initial values
    # (TODO -- ask Tim why 'next' is in url after logging in
    if len(request.GET) and not (len(request.GET) == 1 and 'next' in request.GET):
        
        # copy request.GET into custom QueryDict
        updated_get = QueryDict(mutable=True)
        for k, v in request.GET.items():
                updated_get[k] = v
        
        # if user has deleted keywords, replace with prompt 'Enter keywords...'
        if 'keywords' in updated_get and updated_get['keywords'] == '':
            updated_get['keywords'] = 'Enter keywords...'
        form = ScheduleForm(updated_get)
    else:
        form = ScheduleForm(initial={'keywords': 'Enter keywords...'})
    
    schedule_form = NewScheduleForm(request.GET)
    user_event_form = UserEventForm()
    results = []
    highlight_schedule = True
    num_dept = 0
    num_key = 0
    course_views = []
    user_courses = []   # this will be filled in later by ajax
    user_schedules = []
    context = {}

    #TODO: breaks if student doesn't exist
    current_user = Student.objects.get(user_email=request.user.email)
    
    # if a new user has no schedule, make them their first schedule
    if not current_user.schedule_set.all().exists():
        Schedule.objects.create_schedule("Schedule 1", current_user)
    
    for schedule in current_user.schedule_set.all():
        user_schedules.append(schedule)
    
    
    # these are the course tabs previously opened and stored in a session
    # note that each element of a course_tab must also agree with the format served by
    # make_tab_content()
    course_tabs = []
    if 'tabs' in request.session:
        tabs = request.session['tabs']
        for course_pk in tabs:
            #TODO: this will fail if course doesn't exist
            course = Course.objects.get(pk=course_pk)
            data = get_tab_data(course, request)
            course_tabs.append(get_tab_data(course, request))
    
    #Get the currently active scedule
    schedule_title = None
    if 'active_schedule' in request.session and Schedule.objects.filter(student=current_user).filter(title=request.session['active_schedule']).exists():
        schedule_title = request.session['active_schedule']
    else:
        schedule_title = Schedule.objects.filter(student=current_user)[0].title
        request.session['active_schedule'] = schedule_title
        request.session.save()
    schedule = Schedule.objects.filter(student=current_user).filter(title=schedule_title)[0]
    
    #store whether or not search filters are currently expanded
    filters_expanded = True
    if 'filters_expanded' in request.session:
        filters_expanded = request.session['filters_expanded']
        if filters_expanded == 'true':
            filters_expanded = True
        else:
            filters_expanded = False
    else:
        request.session['filters_expanded'] = filters_expanded
        request.session.save()
    
    results_exist = True
    
    if form.is_valid():
        
        #retrieve all courses in requested term
        term = Term.objects.get(id=form.cleaned_data['course_term'])
        results = Course.objects.select_related().filter(section__term=term).order_by('dept__code', 'number')
        
        #filter based on department
        if form.cleaned_data['departments'] != 'NULL':
            results = results.filter(dept__code=form.cleaned_data['departments'])
        
        #filter based on keywords
        if form.cleaned_data['keywords'] != '':
            keys = form.cleaned_data['keywords']
            title_filter = Q(title__icontains=keys)
            desc_filter = Q(description__icontains=keys)
            
            results = results.filter(title_filter | desc_filter)
        
        #filter based on days
        #if a course has at least one related section with days
        #  containing day, keep it in the results.
        #TODO: this should have more intelligent filtering. What about courses with a lab on Fri, but no lectures?
        #      it probably shouldn't show up, but it will
        days_filter = None
        for day in form.days:
            if form.cleaned_data[day]:
                if days_filter == None:
                    days_filter = Q(section__days__contains=day[:2])
                else:
                    days_filter = days_filter | Q(section__days__contains=day[:2])
        
        if days_filter != None:
            results = results.select_related().filter(days_filter).distinct()
        
        #filter based on course level
        levels_filter = None
        for level in form.levels:
            if form.cleaned_data[level]:
                course_level = level[1]
                if course_level == '5':
                    course_level = '[5-9]'
                regex = r'\w*' + course_level + '\d{2}\w*'
                if levels_filter == None:
                    levels_filter = Q(number__iregex=regex)
                else:
                    levels_filter = levels_filter | Q(number__iregex=regex)
        if levels_filter != None:
            results = results.filter(levels_filter)
            
        #filter based on number of credits
        credits_filter = None
        for credit in form.credits:
            if form.cleaned_data[credit]:
                credit_level = credit[2]
                regex = credit_level + '|[1-' + credit_level +' ]-[' + credit_level + '-9]'
                if credit_level == '5':
                    regex = r'[' + credit_level + '-9]|[1-' + credit_level +' ]-[' + credit_level + '-9]'
                if credits_filter == None:
                    credits_filter = Q(credits__iregex=regex)
                else:
                    credits_filter = credits_filter | Q(credits__iregex=regex)
        if credits_filter != None:
            results = results.filter(credits_filter)
            
        # filter based on whether a course has open sections
        if not form.cleaned_data['closed']:
            results = results.select_related().filter(section__open=True).distinct()
        
        # filter out all non-honors courses
        if form.cleaned_data['honors_only']:
            results = results.filter(honors=True)
        
        # filter based on whether course satisfies one of the requested geneds
        # TODO: order by number of geneds satisfied
        if form.cleaned_data['geneds']:
            geneds = pickle.loads(form.cleaned_data['geneds'])
            gened_filter = None
            any_selected = False
            for gened, selected in geneds.items():
                if selected:
                    any_selected = True
                    if gened_filter == None:
                        gened_filter = Q(gened__code=gened)
                    else:
                        gened_filter = gened_filter | Q(gened__code=gened)
            if any_selected:
                results = results.filter(gened_filter)
                
                
        if form.cleaned_data['start_time']:
            results = results.select_related().filter(section__start__gte=form.cleaned_data['start_time'])
        
        if form.cleaned_data['end_time']:
            results = results.select_related().filter(section__ending__lte=form.cleaned_data['end_time'])
        
        # filter out all courses that conflict with current courses
        if not form.cleaned_data['conflicted']:
            current_courses = ScheduleCourse.objects.filter(schedule=schedule)
            # for every course in results, display it if:
            #   it has at least one section with a time/day that does not conflict with any
            #   of the courses in current_courses
            
            # option 1: regex. option 2: boolean fields
            conflicts = current_courses.values_list('course__days', 'course__start', 'course__ending').distinct()
            #conflicts = current_courses.values_list('course__mon', 'course__tue', 'course__wed', 'course__thu', 'course__fri', 'course__start', 'course__ending').distinct()
            
            #enable for regex:
            days = set()
            for day_set, start, end in conflicts:
                for i in range(0, len(day_set), 2):
                    if not day_set[i:i+2] in days:
                        days.add((day_set[i:i+2], start, end))
            
            
            # A list of tuples which current courses can't conflict with [(day, start, end), ...]
            conflicts = days
            
            
            for section in conflicts:
                # uses regex
                day_filter = Q(section__days__iregex=r'(\w\w)*(' + section[0] + ')(\w\w)*')
                
                #uses boolean fields
                """
                day_filter = None
                if section[0] == True:
                    if day_filter == None:
                        day_filter = Q(section__mon=True)
                    else:
                        day_filter = day_filter | Q(section__mon=True)
                if section[1] == True:
                    if day_filter == None:
                        day_filter = Q(section__tue=True)
                    else:
                        day_filter = day_filter | Q(section__tue=True)
                if section[2] == True:
                    if day_filter == None:
                        day_filter = Q(section__wed=True)
                    else:
                        day_filter = day_filter | Q(section__wed=True)
                if section[3] == True:
                    if day_filter == None:
                        day_filter = Q(section__thu=True)
                    else:
                        day_filter = day_filter | Q(section__thu=True)
                if section[4] == True:
                    if day_filter == None:
                        day_filter = Q(section__fri=True)
                    else:
                        day_filter = day_filter | Q(section__fri=True)
                """
                #regex
                start_filter = Q(section__start__gte=section[2]) # the new course starts after the old course ends
                end_filter = Q(section__ending__lte=section[1])  # the new course ends before the old course starts
                
                #boolean fields
                #start_filter = Q(section__start__gte=section[6]) # the new course starts after the old course ends
                #end_filter = Q(section__ending__lte=section[5])  # the new course ends before the old course starts
                results = results.select_related().exclude(day_filter &  ~(start_filter | end_filter)).distinct()
    
        # Display error - no search results match
        if len(results) == 0:
            results_exist = False
        
    # Todo: can there be too many results? (probably)
    
    # Reformat results to assign each course an index (for js button)
    results = map(lambda r: {'id':r.id, 
                             'title':r.title, 
                             'dept':r.dept,
                             'number':r.number,
                             'description':r.description,
                             'reqs':r.reqs,
                             'lab': r.section_set.exclude(component='lec').exists(),
                             'open': r.section_set.filter(open=True).exists(),
                             'geneds': list(map(lambda g: "{}({})".format(g.code, g.name), r.gened.all())),
                             'conflicts': False, #TODO: implement this
                             'credits': r.credits,
                             'pk': r.pk,
                             }, results)
    
    return render (
        request,
        'schedule.html',
        {'highlight_schedule':highlight_schedule, 'results_exist':results_exist, 'filters_expanded':filters_expanded, 'form':form, 'user_event_form':user_event_form, 'schedule_form':schedule_form, 'results':results, 'course_tabs':course_tabs, 'user_schedules':user_schedules, 'user_courses':user_courses}
    )

#==================================================================#    
#       ^-------------End schedule views------------^
#==================================================================#

from django.shortcuts import render, HttpResponse, redirect

@login_required(login_url='/profile/login/')
def profile(request):

    
    highlight_profile = True
    
    user = request.user
    #TODO: this will break if the student doesn't exist
    student = Student.objects.get(user_email=request.user.email)
    
    return render(
        request,
        'profile.html',
        context={'highlight_profile':highlight_profile, 'student':student, 'user':user}
    )
    
def prereqs(request):

    form = flowchartForm(request.GET)
    course_list = []

    highlight_prereqs = True
    
    #Populate the flowchart
    if form.is_valid(): 
        if(form.cleaned_data['departments'] != 'NULL'):
            course_list = Course.objects.filter(dept__code=form.cleaned_data['departments'])

    #for getting the list of 
    # print(type(course_list))
    # c_list = map(lambda c:{c.title:c.reqs}, course_list)
    # for x in c_list:
    #     print(x)
    # abr = open('abbreviations.txt', 'w')
    # for item in c_list:
    #     abr.write("%s\n" % item)

    #TODO: this should be ajax...
    #format courseNum: [(D)listOfPre(0), (D)levelNumber(1), Selected(2), linked(3), (D)credits(4), (D)required(5), root(6), title(7)]
    #this is a very silly way to tranfser the data but it works for now until I start using ajax.
    course_list = json.dumps(list(map(lambda c: {('title' + str(c.number)):[
                                [int(s) for s in c.reqs.split() if s.isdigit()],#listOfPre(0)... #listOfPre(0)... TODO: this extracts the numbers for the prereqs but does not do complex parsing on things like and and or statements
                                 re.search(r'\d+', c.number).group()[:1],#levelNumber(1)...The regex gets the first number in the course number
                                 0,#Selected(2)...default is 0
                                 0,#linked(3)...default is 0
                                 re.findall('\d+', str(c.credits) ),#credits(4)...a list of numbers extracted from the string because there is sometimes the case of 1-6 credits for independent studies.
                                 1,#required(5)...TODO get required from server right now using temp default to 1 
                                 0,#root(6)]...default is 0
                                 c.title,
                                 form.cleaned_data['departments']
                                 ]
                                 # len(c.reqs.split(" ")),
                                 # c.description]
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
#compsci326
from django.contrib.auth import logout, login, authenticate

def register(request):
    if request.method == 'POST':
        request.POST._mutable = True
        student_form = StudentForm(request.POST)
        user_form = UserForm(request.POST)
        # this links the UserForm and StudentForm:
        request.POST['user_email'] = request.POST['email']
        request.POST._mutable = False
        if user_form.is_valid():
            user_form.save()
            if student_form.is_valid():
                student_form.save()
                new_user = authenticate(
                    username=user_form.cleaned_data['username'],
                    password=user_form.cleaned_data['password1'],
                )
                login(request, new_user)
            
            return profile(request)
        else:
            args = {'user_form':user_form, 'student_form':student_form}
            return render(request, 'registration/registration_form.html', args)
    else:
        user_form = UserForm()
        student_form = StudentForm()
        args = {'user_form':user_form, 'student_form':student_form}
        return render(request, 'registration/registration_form.html', args)

def loginPage(request):
    return render(request, 'registration/login.html', {})

def logoutPage(request):
    return render(request, 'registration/logout.html', {})
    
class CourseDetailView(generic.DetailView):
    """
    lazarus course detail view for use in flowchart
    """
    model = Course
    
    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs) # get the default context data
        context['sections'] = Section.objects.filter(clss=context['course']) # add extra field to the context
        return context