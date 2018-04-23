from django import forms
from django.core.exceptions import ValidationError
from .models import Course, Department, Student, Term, Gened
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import pickle

# ============== START custom widget and field for geneds =================== #
# multivaluefield based off https://gist.github.com/elena/3915748
class MultiWidgetCheckbox(forms.MultiWidget):
    def __init__(self, choices=[], attrs=None):
        self.choices = choices
        widgets = [forms.CheckboxInput() for c in choices]
        super(MultiWidgetCheckbox, self).__init__(widgets, attrs)
        
    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return [False for c in self.choices]
    
    # in-house to avoid dependencies
    # returns a list where each element is a tag
    def parse_html(self, html):
        tags = []
        curr = html
        start = 0
        end = 0
        while '/>' in curr:
            start = curr.index('<')
            end = curr.index('/>') + start
            tags.append(curr[start:end+2])
            curr = curr[end+2:]
        return tags
    
    # This is very fragile!! TODO: make this more robust or probably just migrate to React
    # Also I'm sorry...
    def render(self, name, value, attrs=None):
        html = super(MultiWidgetCheckbox, self).render(name, value, attrs)
        #print(html)
        #print(self.parse_html(html))
        labeled_html = '<div class=\'row\'>'
        tags = self.parse_html(html)
        for i in range(len(tags)):
            if i % 4 == 0:
                if i != 0:
                    labeled_html += '</div>'
                labeled_html += '<div class=\'col-4\'>'
            label = "<label>"+self.choices[i][0]+":</label> "
            labeled_html += label
            labeled_html += tags[i]
            labeled_html += '<br>'
        labeled_html += '</div></div>'
        
        return mark_safe(labeled_html)
    
class MultiBooleanField(forms.MultiValueField):
    
    def __init__(self, choices=[], *args, **kwargs):
        widgets = MultiWidgetCheckbox(choices=choices)
        self.choices = choices
        list_fields = [forms.BooleanField(required=False) for c in choices]
        
        super(MultiBooleanField, self).__init__(list_fields, widget=widgets, *args, **kwargs)

    def compress(self, values):
        result = {}
        for i in range(len(values)):
            result[self.choices[i][0]] = values[i]
        return pickle.dumps(result)
# ============== END custom widget and field for geneds =================== #
        
# form for searching for courses
class ScheduleForm(forms.Form):
    keywords = forms.CharField(required=False, initial="Enter keywords...", help_text="Enter keywords to search for", max_length=200)
    
    depts = list(map(lambda obj: (obj.code, obj.name), Department.objects.all()))
    depts = [('NULL','Pick a department...')] + depts
    departments = forms.TypedChoiceField(choices=depts, coerce=str, initial='NULL', empty_value='NULL', help_text="Enter department to search within")
    
    terms = list(map(lambda term: (term.id, list(filter(lambda season: season[0]==term.season, Term.SEASONS))[0][1] + " " + str(term.year) ), Term.objects.all()))
    course_term = forms.ChoiceField(choices=terms, help_text="Enter term to search within")


    # Sihua's Edit start
    l100 = forms.BooleanField(required=False)
    l200 = forms.BooleanField(required=False)
    l300 = forms.BooleanField(required=False)
    l400 = forms.BooleanField(required=False)
    l500 = forms.BooleanField(required=False)
    levels = ["l100", "l200", "l300", "l400", "l500"]

    cr1 = forms.BooleanField(required=False)
    cr2 = forms.BooleanField(required=False)
    cr3 = forms.BooleanField(required=False)
    cr4 = forms.BooleanField(required=False)
    cr5 = forms.BooleanField(required=False)
    credits = ["cr1", "cr2", "cr3", "cr4", "cr5"]

    closed = forms.BooleanField(required=False)
    conflicted = forms.BooleanField(required=False, initial=True)
    honors_only = forms.BooleanField(required=False)

    Mon = forms.BooleanField(required=False)
    Tus = forms.BooleanField(required=False)
    Wed = forms.BooleanField(required=False)
    Thu = forms.BooleanField(required=False)
    Fri = forms.BooleanField(required=False)
    days = ["Mon", "Tus", "Wed", "Thu", "Fri"]
    
    #Sihua's Edit End
    
    gened_list = list(map(lambda gened: (gened.code, gened.code + ": " + gened.name), Gened.objects.all()))
    
    #see custom field above
    geneds = MultiBooleanField(choices=gened_list, required=False)
    
    
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

# form for creating a new schedule
class NewScheduleForm(forms.Form):
    title = forms.CharField(required=True, max_length=200)
    
    def clean_title(self):
        return self.cleaned_data['title']
        
# form for adding a custom, user event
class UserEventForm(forms.Form):
    title = forms.CharField(required=True, label="Title of event", max_length=50)
    
    mon = forms.BooleanField(required=False, label="Monday")
    tue = forms.BooleanField(required=False, label="Tuesday")
    wed = forms.BooleanField(required=False, label="Wednesday")
    thu = forms.BooleanField(required=False, label="Thursday")
    fri = forms.BooleanField(required=False, label="Friday")
    
    start_time = forms.TimeField(required=True, label="Start time")
    end_time = forms.TimeField(required=True, label="End time")
    
    def clean(self):
        super().clean()
        days = ''
        errors = []
        
        #make sure at least one day is filled in, and reformat to "MoWeFr" etc
        any_selected = False
        if self.cleaned_data['mon']:
            days += 'Mo'
            any_selected = True
        if self.cleaned_data['tue']:
            days += 'Tu'
            any_selected = True
        if self.cleaned_data['wed']:
            days += 'We'
            any_selected = True
        if self.cleaned_data['thu']:
            days += 'Th'
            any_selected = True
        if self.cleaned_data['fri']:
            days += 'Fr'
            any_selected = True
        if not any_selected:
            errors.append(forms.ValidationError("At least one day must be selected.", code='nodays'))
        self.cleaned_data['days'] = days
        
        # make sure start and end times are sequential
        if self.cleaned_data['start_time'] > self.cleaned_data['end_time']:
            errors.append(forms.ValidationError("Start time can't be after end time", code='nodays'))
        
        if len(errors) > 0:
            raise ValidationError(errors)
        
        return self.cleaned_data
    
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
