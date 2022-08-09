from django.conf import settings
from django import forms
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from .forms import CourseCreationForm, ActionCreationForm, StepCreationForm, ProcessCreationForm
from courses.models import Course, Action, Step, ActionPhoto, ActionVideo, Process

"""main client page"""
@login_required
def index(request):
    courses = Course.objects.filter(owner=request.user)
    context = {'courses': courses}
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
def process_creation(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    if request.method == 'POST':
        form = ProcessCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            process = Process.objects.create(course=course,
                                        title=cd['title'],
                                        description=cd['description'],
                                        cover=cd['cover'])
            return redirect('client_interface:process_added', course_slug, process.slug)
        raise print(form.errors)
    form = ProcessCreationForm()
    context = {'courses': courses, 'form': form}
    return render(request, 'client_interface/process_creation.html', context)

@login_required
def process_added(request, course_slug, process_slug):
    courses = Course.objects.filter(owner=request.user)
    process = Process.objects.get(slug=process_slug)
    context = {'courses': courses, 'process': process}
    return render(request, 'client_interface/process_added.html', context)

def process_choices_execute(course_slug, process_slug):
    course = Course.objects.get(slug=course_slug)
    process = Process.objects.get(slug=process_slug)
    queryset = course.process_set.all()
    processes = []
    keys = []
    for process in queryset:
        processes.append(process.title)
        keys.append(process.title)
    process_choices = [(key, process) for key, process in zip(keys, processes)]
    return process_choices

@login_required
def action_creation(request, course_slug, process_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    if request.method == 'POST':
        form = ActionCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            process = Process.objects.get(title=cd['process'])
            action = Action.objects.create(process=process,
                                    title=cd['title'],
                                    main_text=cd['main_text'],
                                    slug=slugify(cd['title']))
            for f in request.FILES.getlist('photos'):
                data = f.read()
                photo = ActionPhoto(action=action)
                photo.photo.save(f.name, ContentFile(data))
                photo.save()
            if cd['video']:
                video = ActionVideo(action=action, video=request.FILES['video'])
                video.save()
            return redirect('client_interface:action_added', course_slug, process.slug, action.slug)
        raise BaseException (form.errors)
    process_choices = process_choices_execute(course_slug, process_slug)
    choice_field = forms.ChoiceField(widget=forms.Select(),
                                     choices=process_choices)
    form = ActionCreationForm(initial={})
    form.fields['process'] = choice_field
    return render(request, 'client_interface/action_creation.html', {'courses': courses, 'course': course, 'form': form})

@login_required
def action_added(request, course_slug, process_slug, action_slug):
    courses = Course.objects.filter(owner=request.user)
    process = Process.objects.get(slug=process_slug)
    action = Action.objects.get(slug=action_slug)
    context = {'courses': courses, 'process': process, 'action': action}
    return render(request, 'client_interface/action_added.html', context)


def action_choices_execute(course_slug, process_slug):
    course = Course.objects.get(slug=course_slug)
    process = Process.objects.get(slug=process_slug)
    queryset = process.action_set.all()
    actions = []
    keys = []
    for action in queryset:
        actions.append(action.title)
        keys.append(action.title)
    action_choices = [(key, action) for key, action in zip(keys, actions)]
    return action_choices

@login_required
def step_creation(request, course_slug, process_slug):
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
                                    slug=slugify(cd['title']))            
            return redirect('client_interface:step_added', course_slug, process_slug, step.slug)
        raise BaseException (form.errors)
    else:
        action_choices = action_choices_execute(course_slug, process_slug)
        choice_field = forms.ChoiceField(widget=forms.Select(),
                                     choices=action_choices,required=False)
        form = StepCreationForm(initial={})
        form.fields['action'] = choice_field
        return render(request, 'client_interface/step_creation.html', {'courses': courses, 'course': course, 'form': form})

@login_required
def step_added(request, course_slug, process_slug, step_slug):
    courses = Course.objects.filter(owner=request.user)
    process = Process.objects.get(slug=process_slug)
    step = Step.objects.get(slug=step_slug)
    action = step.action
    return render(request, 'client_interface/step_added.html', {'courses': courses, 'process': process, 'action': action, 'step': step})


"""showing view """

@login_required
def course_showing(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    processes = course.process_set.all()
    context = {'courses': courses, 'course': course, 'processes': processes}
    return render (request, 'client_interface/course_showing.html', context)

@login_required
def process_showing(request, course_slug, process_slug):
    courses = Course.objects.filter(owner=request.user)
    process = Process.objects.get(slug=process_slug)
    actions = process.action_set.all()
    context = {'courses': courses, 'process': process, 'actions': actions}
    return render(request, 'client_interface/process_showing.html', context)

@login_required
def action_showing(request, course_slug, process_slug, action_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    process = Process.objects.get(slug=process_slug)
    action = Action.objects.get(slug=action_slug)
    steps = action.step_set.all()
    photos = action.photos.all()
    try:
        video = ActionVideo.objects.get(action=action)
        context = {'courses': courses, 'course': course, 'process': process, 'action': action, 'steps': steps, 'photos': photos, 'video': video}
    except:
        context = {'courses': courses, 'course': course, 'process': process, 'action': action, 'steps': steps, 'photos': photos}
    return render(request, 'client_interface/action_showing.html', context)

"""editing"""
@login_required
def course_editing(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.filter(slug=course_slug).first()
    if request.method == 'POST':
        form = CourseCreationForm(instance=course, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_interface:course_showing', course.slug)
    form = CourseCreationForm(instance=course)
    return render(request, 'client_interface/course_edit.html', {'courses': courses, 'course': course, 
                'form': form})

@login_required
def process_editing(request, course_slug, process_slug):
    courses = Course.objects.filter(owner=request.user)
    process = Process.objects.filter(slug=process_slug).first()
    if request.method == 'POST':
        form = ProcessCreationForm(instance=process,data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_interface:course_showing', course_slug)
    form = ProcessCreationForm(instance=process)
    context = {'courses': courses, 'process': process, 'form': form}
    return render(request, 'client_interface/process_edit.html', context)
    
@login_required
def action_editing(request, course_slug, process_slug, action_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.filter(slug=course_slug).first()
    process = Process.objects.filter(slug=process_slug).first()
    action = Action.objects.filter(slug=action_slug).first()
    if request.method == 'POST':
        form = ActionCreationForm(instance=action, data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            action.process = process
            action.title = cd['title']
            action.main_text = cd['main_text']
            action.save()
            for f in request.FILES.getlist('photos'):
                data = f.read()
                photo = ActionPhoto(action=action)
                photo.photo.save(f.name, ContentFile(data))
                photo.save()
            if cd['video']:
                video = ActionVideo(action=action, video=request.FILES['video'])
                video.save() 
            form.save()
            return redirect('client_interface:process_showing', course_slug, process_slug)
    process_choices = process_choices_execute(course_slug, process_slug)
    choice_field = forms.ChoiceField(widget=forms.Select(),
                                     choices=process_choices)
    form = ActionCreationForm(initial={}, instance=action)
    form.fields['process'] = choice_field       
    context = {'courses': courses, 'process': process, 'course': course, 'action': action, 'form': form}
    return render(request, 'client_interface/action_edit.html', context)

@login_required
def step_editing(request, course_slug, action_slug, process_slug, step_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.filter(slug=course_slug).first()
    action = Action.objects.filter(slug=action_slug).first()
    step = Step.objects.filter(slug=step_slug).first()
    if request.method == 'POST':
        form = StepCreationForm(instance=step, data=request.POST, files=request.FILES)
        if form.is_valid():       
            form.save()
            return redirect('client_interface:action_showing', course_slug, process_slug, action_slug)
        print(form.errors)
    action_choices = action_choices_execute(course_slug, process_slug)
    choice_field = forms.ChoiceField(widget=forms.Select(),
                                    choices=action_choices)
    form = StepCreationForm(initial={}, instance=step)
    form.fields['action'] = choice_field
    context = {'courses': courses, 'course': course, 'action': action, 'step': step, 'form': form}
    return render(request, 'client_interface/step_edit.html', context)

"""deleting"""
@login_required
def course_deleting(request, course_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    if request.method == "POST":
        course.delete()
        return redirect('client_interface:index')
    return render(request, 'client_interface/course_deletion.html', {'courses': courses, 'course': course})

@login_required
def process_deleting(request, course_slug, process_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    process = Process.objects.get(slug=process_slug)
    if request.method == 'POST':
        process.delete()
        return redirect('client_interface:course_showing', course.slug)
    context = {'courses': courses, 'course': course, 'process': process}
    return render(request, 'client_interface/process_deletion.html', context)

@login_required
def action_deleting(request, course_slug, process_slug, action_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    process = Process.objects.get(slug=process_slug)
    action = Action.objects.get(slug=action_slug)
    if request.method == 'POST':
        action.delete()
        return redirect('client_interface:process_showing', course_slug, process_slug)
    context = {'courses': courses, 'course': course, 'process': process, 'action': action}
    return render(request, 'client_interface/action_deletion.html', context)

@login_required
def step_deleting(request, course_slug, process_slug, action_slug, step_slug):
    courses = Course.objects.filter(owner=request.user)
    course = Course.objects.get(slug=course_slug)
    process = Process.objects.get(slug=process_slug)
    action = Action.objects.get(slug=action_slug)
    step = Step.objects.get(slug=step_slug)
    if request.method == 'POST':
        step.delete()
        return redirect('client_interface:action_showing', course_slug, process_slug, action_slug)
    context = context = {'courses': courses, 'course': course, 'process': process, 'action': action, 'step': step}
    return render(request, 'client_interface/step_deletion.html', context)
