from django.db import models
from django.urls import reverse
import uuid
import random

import shutil
from django.db.models.signals import post_delete 
from django.dispatch import receiver

# https://stackoverflow.com/questions/1534986/how-do-i-override-delete-on-a-model-and-have-it-still-work-with-related-delete
@receiver(post_delete)
def delete_repo(sender, instance, **kwargs):
    """
    If a ScheduleCourse is being deleted, if it is a user-created event, it should also delete its corresponding Section
    """
    if sender == ScheduleCourse:
        if instance.title != '':
            if ScheduleCourse.objects.filter(course=instance.course).exclude(schedule=instance.schedule).count() == 0:
                instance.course.delete()

class Gened(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a gened category")
    code = models.CharField(max_length=2, help_text="Enter the gened abbreviation")
    
    def __str__(self):
        return "{} ({})".format(self.name, self.code)
        
class Department(models.Model):
    name = models.CharField(max_length=200, blank=True, unique=True, help_text="Enter a department name")
    code = models.CharField(max_length=12, help_text="Enter the department abbreviation")
    
    def __str__(self):
        return "{} ({})".format(self.name, self.code)
    
class Term(models.Model):
    SEASONS = ( 
        ('w', 'Winter'),
        ('t', 'Summer'),
        ('s', 'Spring'),
        ('f', 'Fall'),
    )
    season = models.CharField(max_length=1, choices=SEASONS)
    year = models.IntegerField()
    
    def __str__(self):
        return "{} {}".format(self.season, self.year)
    
class Course(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the descriptive course title")
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, help_text="Enter the course's department")
    number = models.CharField(max_length=6, help_text="Enter the course's title number (220 in COMPSCI 220)")
    description = models.TextField(max_length=1000, help_text="Enter the course description")
    reqs = models.TextField(max_length=1000, blank=True, default="", help_text="Enter the course requirements")
    credits = models.CharField(max_length=4, help_text="Enter # of credits")
    honors = models.BooleanField("Enter whether this class is an honors course")
    CAREERS = (
        ('u', 'Undergraduate'),
        ('g', 'Graduate'),
        ('c', 'Non-Credit'),
        ('d', 'Non-Degree'),
    )
    career = models.CharField(max_length=1, choices=CAREERS, blank=True, default='u', help_text='The course career')
    SESSIONS = (
        ('un', 'University'),
        ('uc', 'University Eligible/CPE'),
        ('ud', 'University Non-standard Dates'),
        ('ce', 'CPE Continuing Education'),
        ('cu', 'CPE Non-Standard Dates'),
        ('c1', 'CPE Summer Session 1'),
        ('c2', 'CPE Summer Session 2'),
        ('c3', 'CPE Summer Session 3'),
    )
    session = models.CharField(max_length=2, choices=SESSIONS, blank=True, default='u', help_text='The course career')
    gened = models.ManyToManyField(Gened, blank=True, help_text='Enter any gened categories this course satisfies')
    start_date = models.DateField(help_text='Enter the starting date of the course')
    end_date = models.DateField(help_text='Enter the ending date of the course')
    
    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])
    
    def __str__(self):
        return "{} {} {}".format(self.dept, self.number, self.title)
        
class SectionManager(models.Manager):
    def create_userevent(self, start_time, end_time, days):
        event = self.create(start=start_time, 
                            ending=end_time, 
                            days=days,
                            term=Term.objects.all()[0],
                            professor=".",
                            room=".",
                            open=True,
                            cap=0,
                            enrolled=0,
                            wcap=0,
                            wenrolled=0,
                            clss=None,
                            component='CUS')
        return event

class Section(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sid = models.IntegerField(default=0, help_text="The 5 digit spire course number") #default=0 for custom events
    days = models.CharField(max_length=10, help_text="Days the course is taught")
    mon = models.BooleanField(blank=True, default=False)
    tue = models.BooleanField(blank=True, default=False)
    wed = models.BooleanField(blank=True, default=False)
    thu = models.BooleanField(blank=True, default=False)
    fri = models.BooleanField(blank=True, default=False)
    start = models.TimeField(help_text='The starting time of the class')
    ending = models.TimeField(help_text='The ending time of the class')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, default=1)
    professor = models.CharField(max_length=200)
    room = models.CharField(max_length=200)
    open = models.BooleanField("Enter whether this class is currently open", default=True)
    cap = models.IntegerField(help_text='The class maximum capacity')
    enrolled = models.IntegerField(help_text='The current number of students enrolled')
    wcap = models.IntegerField(help_text='The maximum size of the waitlist')
    wenrolled = models.IntegerField(help_text='The current size of the waitlist')
    clss = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE, help_text='The corresponding generic class for this section')
    COMPONENTS = (
        ('LEC', 'Lecture'),
        ('DIS', 'Discussion'),
        ('LAB', 'Laboratory'),
        ('COL', 'Colloquium'),
        ('DST', 'Dissertation / Thesis'),
        ('IND', 'Individualized Study'),
        ('PRA', 'Practicum'),
        ('SEM', 'Seminar'),
        ('STS', 'Studio / Skills'),
        ('CUS', 'Custom'),
    )
    component = models.CharField(max_length=3, choices=COMPONENTS)
    
    objects = SectionManager()
    
    def __str__(self):
        return "{} {}".format(self.clss, self.sid)
        
class Student(models.Model):
    user_email = models.EmailField(unique=True, null=False, blank = False,default='')
    USERNAME_FIELD = 'user'
    
    def __str__(self):
        return "{}".format(self.user_email)
    
    
class ScheduleManager(models.Manager):
    def create_schedule(self, title, student):
        schedule = self.create(title=title, student=student)
        return schedule
    
class Schedule(models.Model):
    title = models.CharField(max_length=100, help_text='User-set title for this schedule')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, help_text='The user this schedule belongs to')
    objects = ScheduleManager()
    
    def __str__(self):
        return "{} -- {}".format(self.student, self.title)
    
    
class ScheduleCourseManager(models.Manager):
    def create_schedulecourse(self, course, schedule):
        section = self.create(course=course, schedule=schedule)
        return section

def init_colors():
    return [('red', 'red'),
            ('#157ddf9f', 'blue'),
            ('green', 'green'),
            ('orange', 'orange'),
            ('purple', 'purple'),
            ('pink', 'pink'),
            ('brown', 'brown'),]
        
def get_color():
    colors = init_colors()
    rand = random.randint(0, len(colors)-1)
    return colors[rand][0]
        
class ScheduleCourse(models.Model):
    course = models.ForeignKey(Section, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    COLORS = init_colors()
    color = models.CharField(max_length=15, choices=COLORS, help_text="Enter the color for this course", default=get_color)
    title = models.CharField(max_length=50, help_text="Enter the title of this event", blank=True, default="")
    
    objects = ScheduleCourseManager()
    
    def __str__(self):
        return "{} ({})".format(self.course, self.schedule)