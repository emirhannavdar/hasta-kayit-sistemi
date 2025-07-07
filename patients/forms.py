# patients/forms.py

from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['registration_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}), # HTML5 tarih seçici için
        }