from django import forms
from .models import Movement

class RegisterMovement(forms.ModelForm):
    class Meta:
        model = Movement
        fields = '__all__'