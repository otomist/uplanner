from django.contrib import admin
from .models import Gened, Department, Course, Schedule, User, ScheduleCourse, Term, Section

# Register your models here.

admin.site.register(Gened)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(User)
admin.site.register(Schedule)
admin.site.register(ScheduleCourse)
admin.site.register(Term)
admin.site.register(Section)