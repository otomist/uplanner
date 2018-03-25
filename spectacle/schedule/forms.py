from django import forms
from .models import Course, Department

class ScheduleForm(forms.Form):
    keywords = forms.CharField(required=False, help_text="Enter keywords to search for", max_length=200)
    
    depts = map(lambda obj: (obj.code, obj.name), Department.objects.all())
    #depts=['A', 'B']
    departments = forms.TypedChoiceField(choices=depts, coerce=str, empty_value='', help_text="Enter department to search within")
    
    # cleaning functions -- currently they do nothing
    def clean_keywords(self):
        return self.cleaned_data['keywords']
        
    def clean_departments(self):
        return self.cleaned_data['departments']