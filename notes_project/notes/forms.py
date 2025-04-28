from django import forms
from .models import Notes

class Notesform(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'content']