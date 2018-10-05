from django import forms
from .models import Movement, Exercise

class RegisterMovement(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['name', 'equipment', 'settings']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':True}),
            'equipment' : forms.Select(attrs={'class': 'form-control', 'required':True}),
            'settings' : forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class RegisterExerciseStep1(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'exercise_type', 'description']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':True}),
            'exercise_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3})
        }

class RegisterExerciseStep2(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['goal_value']
        widgets = {
            'goal_value' : forms.NumberInput(attrs={'class': 'form-control', 'required':True}),
        }

class RegisterMovementToExercise(forms.Form):
    pass