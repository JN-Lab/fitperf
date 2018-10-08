from django import forms
from .models import Movement, Exercise

class RegisterExerciseStep1(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'exercise_type', 'description']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':True}),
            'exercise_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3})
        }
