from django import forms
from .models import Course, Department

class ScheduleForm(forms.Form):
    keywords = forms.CharField(required=False, help_text="Enter keywords to search for", max_length=200)
    
    depts = list(map(lambda obj: (obj.code, obj.name), Department.objects.all()))
    depts = [('NULL','')] + depts
    departments = forms.TypedChoiceField(choices=depts, coerce=str, initial='NULL', empty_value='NULL', help_text="Enter department to search within")
    
    
    #Sihua's Edit start 
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
