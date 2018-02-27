from django.db import models

class Gened(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a gened category")
    code = models.CharField(max_length=2, help_text="Enter the gened abbreviation")
    
    def __str__(self):
        return "{} ({})".format(self.name, self.code)
        
class Department(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a department name")
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
    dept = models.ForeignKey(Department, on_delete='CASCADE', help_text="Enter the course's department")
    number = models.CharField(max_length=6, help_text="Enter the course's title number (220 in COMPSCI 220)")
    #sections = models.ForeignKey('Section', help_text="Enter the class's specific lecture sections")
    description = models.TextField(max_length=1000, help_text="Enter the course description")
    reqs = models.TextField(max_length=1000, help_text="Enter the course requirements")
    credits = models.IntegerField(help_text="Enter # of credits")
    honors = models.BooleanField("Enter whether this class is an honors course")
    open = models.BooleanField("Enter whether this class is currently open")
    CAREERS = (
        ('u', 'Undergrad'),
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
    gened = models.ManyToManyField(Gened, help_text='Enter any gened categories this course satisfies')
    start_date = models.DateField(help_text='Enter the starting date of the course')
    end_date = models.DateField(help_text='Enter the ending date of the course')
    
    def __str__(self):
        return "{} {} {}".format(self.dept, self.number, self.title)
    
class Section(models.Model):
    id = models.IntegerField(primary_key=True, help_text="The 5 digit spire course number")
    days = models.CharField(max_length=10, help_text="Days the course is taught")
    start = models.TimeField(help_text='The starting time of the class')
    ending = models.TimeField(help_text='The ending time of the class')
    term = models.ForeignKey(Term, on_delete='CASCADE')
    link = models.CharField(max_length=100, help_text='Link to the spire page for the course')
    professor = models.CharField(max_length=200)
    room = models.CharField(max_length=200)
    cap = models.IntegerField(help_text='The class maximum capacity')
    enrolled = models.IntegerField(help_text='The current number of students enrolled')
    wcap = models.IntegerField(help_text='The maximum size of the waitlist')
    wenrolled = models.IntegerField(help_text='The current size of the waitlist')
    clss = models.ForeignKey(Course, on_delete='CASCADE', help_text='The corresponding generic class for this section')
    COMPONENTS = (
        ('col', 'Colloquium'),
        ('dis', 'Discussion'),
        ('the', 'Dissertation / Thesis'),
        ('stu', 'Individualized Study'),
        ('lab', 'Laboratory'),
        ('lec', 'Lecture'),
        ('pra', 'Practicum'),
        ('sem', 'Seminar'),
        ('ski', 'Studio / Skills'),
    )
    component = models.CharField(max_length=3, choices=COMPONENTS)
    
    def __str__(self):
        return "{} {}".format(self.clss, self.id)
    
class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=16)
    courses = models.ManyToManyField(Section, help_text='The previous courses taken by the user')
    sid = models.CharField(max_length=8, help_text='8 digit spire id')
    major = models.ForeignKey(Department, on_delete='SET_NULL', null=True)
    password = models.CharField(max_length=20)
    credits = models.IntegerField(help_text='The current cumulative number of credits taken')
    
    def __str__(self):
        return "{}".format(self.username)
    
class Schedule(models.Model):
    title = models.CharField(max_length=100, help_text='User-set title for this schedule')
    #courses = models.ForeignKey(ScheduleCourse, on_delete=SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete='CASCADE', help_text='The user this schedule belongs to')
    
    def __str__(self):
        return "{} -- {}".format(self.user, self.title)
    
class ScheduleCourse(models.Model):
    course = models.ForeignKey(Section, on_delete='CASCADE')
    schedule = models.ForeignKey(Schedule, on_delete='CASCADE')
    CATEGORIES = (
        ('w', 'Wishlist'),
        ('a', 'Active'),
    )
    category = models.CharField(max_length=1, choices=CATEGORIES)
    
    def __str__(self):
        return "{}".format(self.course)