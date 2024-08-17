from django import forms
from .models import *


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["start_date", "end_date", "location", "notes"]
        widgets = {
            "start_date": forms.TextInput(attrs={'class': 'form-control datepicker'}),
            "end_date": forms.TextInput(attrs={'class': 'form-control datepicker'}),
            "location": forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }