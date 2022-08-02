from django.test import TestCase, Client
from django.template.defaultfilters import slugify
from django.conf import settings
from courses.models import Course, Action, Step, StepPhoto
from account.models import Account
from client_interface.forms import CourseCreationForm, ActionCreationForm, StepCreationForm


class TestCourseCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))        
        

    def test_form_view_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        response = c.get('/client/course_creation/')        
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        response = c.get('/client/course_creation/')
        self.assertTemplateUsed('client_interface/course_creation.html')

    def test_redirect_is_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        title = 'test title'
        data = {
            'title': title,
            'description': 'test descr',
            'owner': c,    
        }
        form = CourseCreationForm(data=data)
        response = c.post('/client/course_creation/', data=data)
        self.assertRedirects(response, f'/client/{slugify(title)}/course_added/')
        

    def test_course_added_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/course_added/')
        self.assertTemplateUsed('client_interface/course_added.html')

    def test_course_added_content_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/course_added/')
        showed = response.context['course']
        self.assertEqual(showed.title, course.title)

class TestActionCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        

    def test_form_view_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/action_creation/')
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/action_creation/')
        self.assertTemplateUsed('client_interface/action_creation.html')

    def test_redirect_is_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        title = 'test action'
        data = {
            'title': title,
        }
        form = ActionCreationForm(data=data)
        response = c.post(f'/client/{course.slug}/action_creation/', data=data)
        self.assertRedirects(response, f'/client/{course.slug}/{slugify(title)}/action_added/')
        
    def test_action_added_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        action = Action.objects.create(course=course, title='test-action')
        response = c.get(f'/client/{course.slug}/{action.slug}/action_added/')
        self.assertTemplateUsed('client_interface/action_added.html')

    def test_action_added_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        action = Action.objects.create(course=course, title='test-action')
        response = c.get(f'/client/{course.slug}/{action.slug}/action_added/')
        showed_action = response.context['action']
        self.assertEqual(showed_action.course.title, course.title)
        self.assertEqual(showed_action.title, action.title)

class TestStepCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Action.objects.create(course=Course(id=1), title='test-action')
        Action.objects.create(course=Course(id=1), title='test-action2')
        Step.objects.create(action=Action(id=2),title='test step',
                            description='test step descr', main_text='step test text')

    def test_form_view_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/step_creation/')
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/step_creation/')
        self.assertTemplateUsed('client_interface/step_creation.html')

    def test_redirect_is_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
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
        response = c.post(f'/client/{course.slug}/step_creation/', data=data)
        self.assertRedirects(response, f'/client/{course.slug}/{slugify(title)}-2/step_added/')

    def test_step_added_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        action = Action.objects.get(title='test-action2')
        step = Step.objects.get(action=action)
        response = c.get(f'/client/{course.slug}/{step.slug}/step_added/')
        self.assertTemplateUsed('client_interface/step_added.html')

    def test_step_added_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        action = Action.objects.get(title='test-action2')
        step = Step.objects.get(action=action)
        response = c.get(f'/client/{course.slug}/{step.slug}/step_added/')
        showed = response.context['step']
        self.assertEqual(showed.title, step.title)

class TestAllCoursesShowingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Course.objects.create(title='test2', description='test descr2', owner=Account(id=1))

    def test_all_courses_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        courses = Course.objects.filter(owner=Account(id=1))
        response = c.get('/client/all_courses/')
        self.assertEqual(response.status_code, 200)
    
    def test_all_courses_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        response = c.get('/client/all_courses/')
        self.assertTemplateUsed('client_interface/all_courses.html')

    def test_all_courses_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        courses = Course.objects.filter(owner=Account(id=1))
        course = Course.objects.get(id=1)
        response = c.get(f'/client/all_courses/')
        showed_course = response.context['courses'][0]
        self.assertEqual(showed_course.title, course.title)
        self.assertEqual(showed_course.description, course.description)
        self.assertTrue(len(response.context['courses']) == len(courses))
        


class TestCourseShowingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Action.objects.create(course=Course(id=1), title='test-action')
        Action.objects.create(course=Course(id=1), title='test-action2')
        Step.objects.create(action=Action(id=2),title='test step',
                            description='test step descr', main_text='step test text')

    def test_course_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/courses/show/{course.slug}/')
        self.assertEqual(response.status_code, 200)


    def test_course_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/courses/show/{course.slug}/')
        self.assertTemplateUsed('client_interface/course_showing.html')


    def test_course_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        action = Action.objects.get(id=2)
        step = Step.objects.get(id=1)
        response = c.get(f'/client/courses/show/{course.slug}/')
        showed_course = response.context['course']
        showed_first_action = response.context['actions'][1]
        showed_first_step = response.context['steps'][0]
        self.assertEqual(showed_course.title, course.title)
        self.assertEqual(showed_course.description, course.description)
        self.assertEqual(showed_first_action.title, action.title)
        self.assertEqual(showed_first_step.title, step.title)
        self.assertEqual(showed_first_step.description, step.description)
        self.assertEqual(showed_first_step.main_text, step.main_text)
        


        
    

    
        

        

    
