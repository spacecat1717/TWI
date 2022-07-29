from django.test import TestCase
from courses.models import Course, Action, Step
from django.template.defaultfilters import slugify

class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', cover=None)
    
    def test_get_absolute_url(self):
        course = Course.objects.get(id=1)
        self.assertEquals(course.get_absolute_url(), f'/courses/{course.slug}/')

class ActionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', cover=None)
        Action.objects.create(course=Course(id=1), title='test action', cover=None)
    
    def test_slug_is_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course)
        self.assertEquals(action.slug, slugify(action.title))

class StepModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', cover=None)
        Action.objects.create(course=Course(id=1), title='test action', cover=None)
        Step.objects.create(action=Action(id=1), title='test step', description='test desc', main_text='test text')

    def test_slug_is_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course)
        step = Step.objects.get(action=action)
        self.assertEquals(step.slug, slugify(step.title)) 

