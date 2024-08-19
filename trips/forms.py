from django import forms
from .models import *


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ["location", "start_date", "end_date", "notes"]
        widgets = {
            "location": forms.Select(attrs={'class': 'form-control'}),
            "start_date": forms.TextInput(attrs={'class': 'form-control datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        
        if start_date and end_date and start_date > end_date:
            self.add_error("end_date", "End date cannot be earlier than the start date.")
        
        return cleaned_data
