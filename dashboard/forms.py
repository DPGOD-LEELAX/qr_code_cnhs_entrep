from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fname', 'lname', 'phone_no', 'full_address', 'strand', 'section', 'school', 'guardian_phone']
        widgets = {
            'strand': forms.Select(attrs={'class': 'form-select'}),
        }
