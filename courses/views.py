from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Action, Step, ActionPhoto, ActionVideo, Process



"""main page"""
def index(request):
    return render(request, 'courses/index.html')


"""showing views"""
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'courses': courses})

def course_view(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    processes = course.process_set.all()
    return render(request, 'courses/course.html', {'course': course, 'processes': processes})

def process_view(request, course_slug, process_slug):
    process = Process.objects.get(slug=process_slug)
    actions = process.action_set.all()
    return render (request, 'courses/process.html', {'process': process,'actions': actions})

def action_view(request, course_slug, process_slug, action_slug):
    action = Action.objects.get(slug=action_slug)
    steps = action.step_set.all()
    photos = action.photos.all()
    video = action.video.all()
    context = {'action': action, 'steps': steps, 'photos': photos, 'video': video}
    return render(request, 'courses/action.html', context)

