from django import forms
from .models import Movement

class RegisterMovement(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['name', 'equipment', 'settings']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':True}),
            'equipment' : forms.Select(attrs={'class': 'form-control', 'required':True}),
            'settings' : forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }