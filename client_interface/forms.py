from django import forms
from courses.models import Course, Action, Step


class CourseCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    cover = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Course
        fields = ['title', 'description', 'cover']
    

class ActionCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput)
    cover = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Action
        fields = ['title', 'cover']

class StepCreationForm(forms.ModelForm):
    action = forms.CharField(required=False)
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=255)
    main_text = forms.CharField(max_length=5000, widget=forms.Textarea)
    photos = forms.ImageField(widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)
    video = forms.FileField(widget=forms.FileInput, required=False)
    class Meta:
        model = Step
        fields = ['title', 'description', 'main_text', 'photos', 'video']
