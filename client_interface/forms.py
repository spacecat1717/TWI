from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from courses.models import Course, Action, Step, Process, ActionPhoto, ActionVideo


class CourseCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    cover = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Course
        fields = ['title', 'description', 'cover']

class ProcessCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput)  
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    cover = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Process
        fields = ['title', 'description', 'cover']  

class ActionCreationForm(forms.ModelForm):
    process = forms.CharField(max_length=128) 
    title = forms.CharField(max_length=128, widget=forms.TextInput)
    cover = forms.ImageField(widget=forms.FileInput, required=False)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    photos = forms.ImageField(widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)
    video = forms.FileField(widget=forms.FileInput, required=False)
    class Meta:
        model = Action
        fields = ['title', 'description', 'cover']

class StepCreationForm(forms.ModelForm):
    action = forms.CharField(max_length=128, required=False)
    step_title = forms.CharField(max_length=128, widget=forms.TextInput)
    key_moment = forms.CharField(max_length=256, widget=forms.Textarea)
    key_moment_reason = forms.CharField(max_length=1000, widget=forms.Textarea)
    class Meta:
        model = Step
        fields = ['step_title', 'key_moment', 'key_moment_reason']





