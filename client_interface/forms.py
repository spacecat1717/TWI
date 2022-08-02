from django import forms
from courses.models import Course, Action, Step


class CourseCreationForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    cover = forms.ImageField(widget=forms.FileInput, required=False)
    

class ActionCreationForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput)
    cover = forms.ImageField(widget=forms.FileInput, required=False)

class StepCreationForm(forms.Form):
    action = forms.CharField()
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=255)
    text = forms.CharField(max_length=5000, widget=forms.Textarea)
    photos = forms.ImageField(widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)
