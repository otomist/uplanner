from django import forms


class ScheduleForm(forms.Form):
    search_keywords = forms.CharField(required=False, help_text="Enter keywords to search for", max_length=200)
    
    def clean_search_keywords(self):
        return self.cleaned_data['search_keywords']