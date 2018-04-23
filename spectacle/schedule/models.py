from django.db import models
from django.urls import reverse
import uuid

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
    credits = models.CharField(max_length=3, help_text="Enter # of credits")
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
        ('c1', 'CPE Summer Session 1'),
        ('c2', 'CPE Summer Session 2'),
        ('c3', 'CPE Summer Session 3'),
    )
    session = models.CharField(max_length=2, choices=SESSIONS, blank=True, default='u', help_text='The course career')
    gened = models.ManyToManyField(Gened, blank=True, help_text='Enter any gened categories this course satisfies')
    start_date = models.DateField(help_text='Enter the starting date of the course')
    end_date = models.DateField(help_text='Enter the ending date of the course')
    
    def get_absolute_url(self):
        return reverse('course-detail', args=[str(self.id)])
    
    def __str__(self):
        return "{} {} {}".format(self.dept, self.number, self.title)
    
class Section(models.Model):
    id = models.IntegerField(primary_key=True, help_text="The 5 digit spire course number")
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
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
    
    def __str__(self):
        return "{} {}".format(self.clss, self.id)
        
class Student(models.Model):
    user_email = models.EmailField(unique=True, null=False, blank = False,default='')
    courses = models.ManyToManyField(Section, blank=True, help_text='The previous courses taken by the user')
    sid = models.CharField(max_length=8, help_text='8 digit spire id')
    major = models.ForeignKey(Department, on_delete='SET_NULL', null=True)
    credits = models.IntegerField(help_text='The current cumulative number of credits taken')
    USERNAME_FIELD = 'user'
        
    def __str__(self):
        return "{} {} {}".format(self.user_email, self.sid, self.major)
    
class ScheduleManager(models.Manager):
    def create_schedule(self, title, student):
        schedule = self.create(title=title, student=student)
        return schedule
    #def create_temp_schedule(self):
    
    
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
    
class ScheduleCourse(models.Model):
    course = models.ForeignKey(Section, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    color = models.CharField(max_length=15, help_text="Enter the color for this course", default="#157ddf9f")
    title = models.CharField(max_length=50, help_text="Enter the title of this event", blank=True, default="")
    
    objects = ScheduleCourseManager()
    
    def __str__(self):
        return "{} ({})".format(self.course, self.schedule)