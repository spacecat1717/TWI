from django.test import TestCase
from courses.models import Course, Action, Step, Process
from django.template.defaultfilters import slugify

class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', cover=None)
    
    def test_get_absolute_url(self):
        course = Course.objects.get(id=1)
        self.assertEquals(course.get_absolute_url(), f'/courses/{course.slug}/')

class ProcessModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', cover=None)
        Process.objects.create(course=Course(id=1), title='test proc', description='test desc')

    def test_slug_is_correct(self):
        course = Course.objects.get(id=1)
        process = Process.objects.filter(course=course).first()
        self.assertEquals(process.slug, slugify(process.title))

class ActionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', cover=None)
        Process.objects.create(course=Course(id=1), title='test proc', description='test descr')
        Action.objects.create(process=Process(id=1), title='test action', main_text='test text')
    
    def test_slug_is_correct(self):
        course = Course.objects.get(id=1)
        process = Process.objects.filter(course=course).first()
        action = Action.objects.get(process=process)
        self.assertEquals(action.slug, slugify(action.title))

class StepModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', cover=None)
        Process.objects.create(course=Course(id=1), title='test proc', description='test descr')
        Action.objects.create(process=Process(id=1), title='test action', main_text='test text')
        Step.objects.create(action=Action(id=1), title='test step', description='test desc')

    def test_slug_is_correct(self):
        course = Course.objects.get(id=1)
        process = Process.objects.filter(course=course).first()
        action = Action.objects.get(process=process)
        step = Step.objects.get(action=action)
        self.assertEquals(step.slug, slugify(step.title)) 

