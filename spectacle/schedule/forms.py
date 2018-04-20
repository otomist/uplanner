from django import forms
from django.core.exceptions import ValidationError
from .models import Course, Department, Student, Term
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ScheduleForm(forms.Form):
    keywords = forms.CharField(required=False, initial="Enter keywords...", help_text="Enter keywords to search for", max_length=200)
    
    depts = list(map(lambda obj: (obj.code, obj.name), Department.objects.all()))
    depts = [('NULL','Pick a department...')] + depts
    departments = forms.TypedChoiceField(choices=depts, coerce=str, initial='NULL', empty_value='NULL', help_text="Enter department to search within")
    
    terms = list(map(lambda term: (term.id, list(filter(lambda season: season[0]==term.season, Term.SEASONS))[0][1] + " " + str(term.year) ), Term.objects.all()))
    course_term = forms.ChoiceField(choices=terms, help_text="Enter term to search within")


    # Sihua's Edit start
    # Note: I replaced all checkboxes, but I need help to determine the search keys for course level, credits, course_status.They are not straight as weekdays constrains.
    l100 = forms.BooleanField(required=False)
    l200 = forms.BooleanField(required=False)
    l300 = forms.BooleanField(required=False)
    l400 = forms.BooleanField(required=False)
    # Note: 500+ needs more than one keys to search or is there a better way for level?
    l500 = forms.BooleanField(required=False)
    levels = ["l100", "l200", "l300", "l400", "l500"]

    # 1 credit, I tried to use 1cr as variable name but failed. 
    cr1 = forms.BooleanField(required=False)
    cr2 = forms.BooleanField(required=False)
    cr3 = forms.BooleanField(required=False)
    cr4 = forms.BooleanField(required=False)
    cr5 = forms.BooleanField(required=False)
    credits = ["cr1", "cr2", "cr3", "cr4", "cr5"]

    closed = forms.BooleanField(required=False)
    conflicted = forms.BooleanField(required=False, initial=True)
    honors_only = forms.BooleanField(required=False)

    # need checkbox for every day and will return True or False
    Mon = forms.BooleanField(required=False)
    Tus = forms.BooleanField(required=False)
    Wed = forms.BooleanField(required=False)
    Thu = forms.BooleanField(required=False)
    Fri = forms.BooleanField(required=False)
    # a list of False or True from checkbox
    days = ["Mon", "Tus", "Wed", "Thu", "Fri"]
    
    #Sihua's Edit End
	
    # make either departments or keywords mandatory; at least one must be filled in
    def clean(self):
        super().clean()
        
        if self.cleaned_data.get('keywords') == "Enter keywords...":
            self.cleaned_data['keywords'] = ''
        
        department = self.cleaned_data.get('departments')
        keywords = self.cleaned_data.get('keywords')
        
        if department == 'NULL' and keywords == '':
            msg = forms.ValidationError("Values must be given for \"keywords\", \"departments\", or both.", code='blank')            
            raise ValidationError([
                msg,
            ])
            
        else:
            return self.cleaned_data

class NewScheduleForm(forms.Form):
    title = forms.CharField(required=True, max_length=200)
    
    def clean_title(self):
        return self.cleaned_data['title']
        
class flowchartForm(forms.Form):
	depts = map(lambda obj: (obj.code, obj.name), Department.objects.all())
	
	departments = forms.TypedChoiceField(choices=depts, coerce=str, empty_value='', help_text="Enter Department")

class StudentForm(forms.ModelForm):
    error_css_class = "error"
    sid = forms.CharField(max_length=8, required=True)
    credits = forms.IntegerField(required=True)
    user_email = forms.EmailField(widget = forms.HiddenInput(), required=False)
    class Meta:
        model = Student
        fields = {
            'sid',
            'credits',
            'user_email',
            'major',
        }
    
    def save(self, commit=True):
        student = super(StudentForm, self).save(commit=False)
        student.sid = self.cleaned_data['sid']
        student.credits = self.cleaned_data['credits']
        student.user_email = self.cleaned_data['user_email']
        if commit:
            student.save()

        return student
    
class UserForm(UserCreationForm):
    error_css_class = "error"
    first_name = forms.CharField(max_length = 30, required=True)
    last_name = forms.CharField(max_length = 30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'email',
        )
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
