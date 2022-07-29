from django.conf import settings
from django import forms
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from .forms import CourseCreationForm, ActionCreationForm, StepCreationForm
from courses.models import Course, Action, Step, StepPhoto

"""main client page"""
def index(request):
    return render(request, 'client_interface/index.html')


"""course creation views"""
def course_creation(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            course = Course.objects.create(title=cd['title'],
            description=cd['description'],
            cover=cd['cover'],
            slug=slugify(cd['title']))
            return redirect('client_interface:course_added', course.slug)
    else:        
        form = CourseCreationForm()
        return render(request, 'client_interface/course_creation.html', {'form': form})

def course_added(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    return render(request, 'client_interface/course_added.html', {'course': course})


def action_creation(request, course_slug):
    if request.method == 'POST':
        form = ActionCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            course = Course.objects.get(slug=course_slug)
            action = Action.objects.create(course=course,
                                        title=cd['title'],
                                        cover=cd['cover'],
                                        slug=slugify(cd['title']))
            return redirect('client_interface:action_added', course.slug, action.slug)
        else:print(form.errors)

    else:
        course = Course.objects.get(slug=course_slug)
        form = ActionCreationForm()
        return render(request, 'client_interface/action_creation.html', {'course': course, 'form': form})

def action_added(request, course_slug, action_slug):
    action = Action.objects.get(slug=action_slug)
    return render(request, 'client_interface/action_added.html', {'action': action})


def action_choices_execute(course_slug):
    course = Course.objects.get(slug=course_slug)
    queryset = course.action_set.all()
    actions = []
    action_choices = []
    keys = []
    for action in queryset:
        actions.append(action.title)
        keys.append(action.title)
    action_choices = [(key, action) for key, action in zip(keys, actions)]
    print('choices', action_choices)
    return action_choices

def step_creation(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    if request.method == 'POST':
        form = StepCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            action = Action.objects.get(title=cd['action'])
            step = Step.objects.create(action=action,
                                    title=cd['title'],
                                    description=cd['description'],
                                    main_text=cd['text'],
                                    slug=slugify(cd['title'])) 
                
            for f in request.FILES.getlist('photos'):
                data = f.read()
                photo = StepPhoto(step=step)
                photo.photo.save(f.name, ContentFile(data))
                photo.save()                   
            return redirect('client_interface:step_added', course.slug, step.slug)
        else:
            print(form.errors)
    else:
        action_choices = action_choices_execute(course_slug)
        choice_field = forms.ChoiceField(widget=forms.Select(),
                                     choices=action_choices)
        form = StepCreationForm(initial={})
        form.fields['action'] = choice_field
        return render(request, 'client_interface/step_creation.html', {'course': course, 'form': form})

def step_added(request, course_slug, step_slug):
    step = Step.objects.get(slug=step_slug)
    return render(request, 'client_interface/step_added.html', {'step': step})
