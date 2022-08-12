from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
import datetime, pytils
from account.models import Account


class Course(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)
    cover = models.ImageField(upload_to = 'media/courses/covers/static/', null=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return f'/courses/{self.title}/'

    def __str__(self):
        return self.title


class Process(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    cover = models.ImageField(upload_to = 'media/courses/covers/static/', null=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('process', kwargs={'process_slug': self.slug})

    def __str__(self):
        return self.title

class Action(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(upload_to = 'media/courses/covers/static/', null=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    

    def get_absolute_url(self):
        return reverse('action', kwargs={'action_slug': self.slug})

    def __str__(self):
        return self.title


class Step(models.Model):
    action = models.ForeignKey(Action, related_name='step', on_delete=models.CASCADE)
    step_title = models.CharField(max_length=100)
    key_moment = models.CharField(max_length=250)
    key_moment_reason = models.CharField(max_length=250, null=True)
    slug = AutoSlugField(populate_from='step_title', unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('step', kwargs={'step_slug': self.slug})

    def __str__(self):
        return self.title


class ActionPhoto(models.Model):
    photo = models.ImageField(upload_to = 'media/courses/actions/photos/static/', null=True)
    action = models.ForeignKey(Action, related_name='photos', on_delete=models.CASCADE, default=1)

class ActionVideo(models.Model):
    video = models.FileField(upload_to='media/courses/actions/videos/', null=True)
    action = models.ForeignKey(Action, related_name='video', on_delete=models.CASCADE, default=1)