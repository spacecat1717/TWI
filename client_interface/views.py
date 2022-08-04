from django.conf import settings
from django import forms
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from .forms import CourseCreationForm, ActionCreationForm, StepCreationForm
from courses.models import Course, Action, Step, StepPhoto, StepVideo

"""main client page"""
@login_required
def index(request):
    courses = Course.objects.filter(owner=request.user)
    actions = Action.objects.filter(owner=request.user)
    steps = Step.objects.filter(owner=request.user)
    context = {'courses': courses, 'actions': actions, 'steps': steps}
    return render(request, 'client_interface/index.html', context)


"""course creation views"""
@login_required
def course_creation(request):
    courses = Course.objects.filter(owner=request.user)
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            course = Course.objects.create(title=cd['title'],
            description=cd['description'],
            cover=cd['cover'],
            slug=slugify(cd['title']),
            owner=request.user)
            return redirect('client_interface:course_added', course.slug)
        raise ValidationError(_(form.errors))
    form = CourseCreationForm()
    return render(request, 'client_interface/course_creation.html', {'courses': courses, 'form': form})

@login_required
def course_added(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    return render(request, 'client_interface/course_added.html', {'courses': courses, 'course': course})


@login_required
def action_creation(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
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
        raise ValidationError(_(form.errors))
    else:
        form = ActionCreationForm()
        return render(request, 'client_interface/action_creation.html', {'courses': courses, 'form': form})

@login_required
def action_added(request, course_slug, action_slug):
    courses = Course.objects.filter(owner=request.user)
    action = Action.objects.get(slug=action_slug)
    return render(request, 'client_interface/action_added.html', {'courses': courses, 'action': action})


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
    return action_choices

@login_required
def step_creation(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
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
            if cd['video']:
                video = StepVideo(step=step, video=request.FILES['video'])
                video.save()              
            return redirect('client_interface:step_added', course.slug, step.slug)
        raise ValidationError(_(form.errors))
    else:
        action_choices = action_choices_execute(course_slug)
        choice_field = forms.ChoiceField(widget=forms.Select(),
                                     choices=action_choices)
        form = StepCreationForm(initial={})
        form.fields['action'] = choice_field
        return render(request, 'client_interface/step_creation.html', {'courses': courses, 'course': course, 'form': form})

@login_required
def step_added(request, course_slug, step_slug):
    courses = Course.objects.filter(owner=request.user)
    step = Step.objects.get(slug=step_slug)
    return render(request, 'client_interface/step_added.html', {'courses': courses, 'step': step})


"""showing view """

@login_required
def all_courses(request):
    courses = Course.objects.filter(owner=request.user)
    return render(request, 'client_interface/all_courses.html', {'courses': courses})

@login_required
def course_showing(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    actions = course.action_set.all()
    steps = Step.objects.all()
    photos = StepPhoto.objects.all()
    step_counter = 0
    for step in steps:
        step_counter += 1
    context = {'courses': courses, 'course': course, 'actions': actions, 
                'steps': steps, 'photos': photos, 'step_counter': step_counter}
    return render (request, 'client_interface/course_showing.html', context)


