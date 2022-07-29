from django.test import TestCase
from django.template.defaultfilters import slugify
from courses.models import Course, Action, Step
from client_interface.forms import CourseCreationForm, ActionCreationForm, StepCreationForm


class TestCourseCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr')
        
    
    def test_form_view_url_exists(self):
        response = self.client.get('/client/course_creation/')
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        self.assertTemplateUsed('client_interface/course_creation.html')

    def test_redirect_is_correct(self):
        title = 'test title'
        data = {
            'title': title,
            'description': 'test descr',    
        }
        form = CourseCreationForm(data=data)
        response = self.client.post('/client/course_creation/', data=data)
        self.assertRedirects(response, f'/client/{slugify(title)}/course_added/')
        

    def test_course_added_template_correct(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/client/{course.slug}/course_added/')
        self.assertTemplateUsed('client_interface/course_added.html')

    def test_course_added_content_correct(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/client/{course.slug}/course_added/')
        showed = response.context['course']
        self.assertEqual(showed.title, course.title)

class TestActionCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr')

    def test_form_view_url_exists(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/client/{course.slug}/action_creation/')
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/client/{course.slug}/action_creation/')
        self.assertTemplateUsed('client_interface/action_creation.html')

    def test_redirect_is_correct(self):
        course = Course.objects.get(id=1)
        title = 'test action'
        data = {
            'title': title,
        }
        form = ActionCreationForm(data=data)
        response = self.client.post(f'/client/{course.slug}/action_creation/', data=data)
        self.assertRedirects(response, f'/client/{course.slug}/{slugify(title)}/action_added/')
        
    def test_action_added_template_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.create(course=course, title='test-action')
        response = self.client.get(f'/client/{course.slug}/{action.slug}/action_added/')
        self.assertTemplateUsed('client_interface/action_added.html')

    def test_action_added_context_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.create(course=course, title='test-action')
        response = self.client.get(f'/client/{course.slug}/{action.slug}/action_added/')
        showed_action = response.context['action']
        self.assertEqual(showed_action.course.title, course.title)
        self.assertEqual(showed_action.title, action.title)

class TestStepCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr')
        Action.objects.create(course=Course(id=1), title='test-action')
        Action.objects.create(course=Course(id=1), title='test-action2')
        Step.objects.create(action=Action(id=2),title='test step',
                            description='test step descr', main_text='step test text')

    def test_form_view_url_exists(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/client/{course.slug}/step_creation/')
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/client/{course.slug}/step_creation/')
        self.assertTemplateUsed('client_interface/step_creation.html')

    def test_redirect_is_correct(self):
        course = Course.objects.get(id=1)
        title = 'test step'
        desc = 'test step descr'
        text = 'test step text'
        data = {
            'action': 'test-action2',
            'title': title,
            'description': desc,
            'text': text,
            }
        form = StepCreationForm(data=data)
        response = self.client.post(f'/client/{course.slug}/step_creation/', data=data)
        self.assertRedirects(response, f'/client/{course.slug}/{slugify(title)}-2/step_added/')

    def test_step_added_template_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(title='test-action2')
        step = Step.objects.get(action=action)
        response = self.client.get(f'/client/{course.slug}/{step.slug}/step_added/')
        self.assertTemplateUsed('client_interface/step_added.html')

    def test_step_added_context_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(title='test-action2')
        step = Step.objects.get(action=action)
        response = self.client.get(f'/client/{course.slug}/{step.slug}/step_added/')
        showed = response.context['step']
        self.assertEqual(showed.title, step.title)

        #test
        
    

    
        

        

    
