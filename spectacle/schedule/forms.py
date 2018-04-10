from django import forms
from .models import Course, Department
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ScheduleForm(forms.Form):
    keywords = forms.CharField(required=False, help_text="Enter keywords to search for", max_length=200)
    
    depts = list(map(lambda obj: (obj.code, obj.name), Department.objects.all()))
    depts = [('NULL','')] + depts
    departments = forms.TypedChoiceField(choices=depts, coerce=str, initial='NULL', empty_value='NULL', help_text="Enter department to search within")
    
    
    # Sihua's Edit start
    # Note: I replaced all checkboxes, but I need help to determine the search keys for course level, credits, course_status.They are not straight as weekdays constrains.
    l100 = forms.BooleanField(required=False)
    l200 = forms.BooleanField(required=False)
    l300 = forms.BooleanField(required=False)
    l400 = forms.BooleanField(required=False)
    # Note: 500+ needs more than one keys to search or is there a better way for level?
    l500 = forms.BooleanField(required=False)
    levels = [l100, l200, l300, l400, l500]

    # 1 credit, I tried to use 1cr as variable name but failed. 
    cr1 = forms.BooleanField(required=False)
    cr2 = forms.BooleanField(required=False)
    cr3 = forms.BooleanField(required=False)
    cr4 = forms.BooleanField(required=False)
    cr5 = forms.BooleanField(required=False)
    credits = [cr1, cr2, cr3, cr4, cr5]

    closed = forms.BooleanField(required=False)
    conflicted = forms.BooleanField(required=False)
    unmet_req = forms.BooleanField(required=False)
    honors_only = forms.BooleanField(required=False)
    course_cat = [closed, conflicted, unmet_req, honors_only]

    # need checkbox for every day and will return True or False
    Mon = forms.BooleanField(required=False)
    Tus = forms.BooleanField(required=False)
    Wed = forms.BooleanField(required=False)
    Thu = forms.BooleanField(required=False)
    Fri = forms.BooleanField(required=False)
    # a list of False or True from checkbox
    days = [Mon, Tus, Wed, Thu, Fri]
    
    
    # a function to change a list of True or False to keys for searching
    def get_daykeys(days):
        dayKeys = ["Mo", "Tu", "We", "Th", "Fr"]
        finalKeys = []
        for x in range(5):
            if days[x]:
                finalKeys.append(dayKeys[x])
        if len(finalKeys) == 0:
            return dayKeys
        return finalKeys
    
    days = get_daykeys(days)
    #Sihua's Edit End
	
    # cleaning functions -- currently they do nothing
    def clean_keywords(self):
        return self.cleaned_data['keywords']
        
    def clean_departments(self):
        return self.cleaned_data['departments']

class NewScheduleForm(forms.Form):
    title = forms.CharField(required=True, max_length=200)
    
    def clean_title(self):
        return self.cleaned_data['title']
        
class flowchartForm(forms.Form):
	depts = map(lambda obj: (obj.code, obj.name), Department.objects.all())
	
	departments = forms.TypedChoiceField(choices=depts, coerce=str, empty_value='', help_text="Enter Department")

class userRegistration(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        }
    
    def save(self, commit=True):
        user = super(userRegistration, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
