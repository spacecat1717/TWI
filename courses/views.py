from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage #is this important???
from .models import Course, Action, Step


"""main page"""
def index(request):
    return render(request, 'courses/index.html')


"""showing views"""
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'courses': courses})

def course_view(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    course_actions = course.action_set.order_by('title')
    context = {'course': course, 'course_actions': course_actions}
    return render(request, 'courses/course.html', context)

def action_view(request, course_slug, action_slug):
    course = get_object_or_404(Course, slug=course_slug)
    action = get_object_or_404(Action, slug=action_slug)
    steps = action.step_set.order_by('title')
    context = {'course': course, 'action': action, 'steps': steps}
    #TODO: add photo!
    return render(request, 'courses/action.html', context)

def step_view(request, course_slug, action_slug, step_slug):
    course = get_object_or_404(Course, slug=course_slug)
    action = get_object_or_404(Action, slug=action_slug)
    step = get_object_or_404(Step, slug=step_slug)
    #TODO:add photo!!!!
    context = {'course': course, 'action': action, 'step': step}
    return render(request, 'courses/step.html', context)