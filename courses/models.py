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


class Action(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to = 'media/courses/actions/covers/static/', null=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('action', kwargs={'action_slug': self.slug})

    def __str__(self):
        return self.title


class Step(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    main_text = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('step', kwargs={'step_slug': self.slug})

    def __str__(self):
        return self.title


class StepPhoto(models.Model):
    photo = models.ImageField(upload_to = 'media/courses/actions/photos/static/', null=True)
    step = models.ForeignKey(Step, related_name='photos', on_delete=models.CASCADE, default=1)

class StepVideo(models.Model):
    video = models.FileField(upload_to='media/courses/actions/videos/', null=True)
    step = models.ForeignKey(Step, related_name='video', on_delete=models.CASCADE, default=1)