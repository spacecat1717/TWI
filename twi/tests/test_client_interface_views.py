from django.test import TestCase, Client
from django.template.defaultfilters import slugify
from django.conf import settings
from courses.models import Course, Action, Step, Process
from account.models import Account
from client_interface.forms import CourseCreationForm, ActionCreationForm, StepCreationForm, ProcessCreationForm


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

class TestProcessCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test proc', description='test descr')

    def test_form_view_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/process_creation/')
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/process_creation/')
        self.assertTemplateUsed('client_interface/process_creation.html')

    def test_redirect_is_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        title = 'test proc title'
        data = {
            'course': course,
            'title': title,
            'description': 'test desc',
        }
        form = ProcessCreationForm(data=data)
        response = c.post(f'/client/{course.slug}/process_creation/', data=data)
        self.assertRedirects(response, f'/client/{course.slug}/{slugify(title)}/process_added/')

    def test_process_added_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/{process.slug}/process_added/')
        self.assertTemplateUsed('client_interface/process_added.html')

    def test_process_added_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/{process.slug}/process_added/')
        showing_process = response.context['process']
        self.assertEqual(showing_process.title, process.title)

class TestActionCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test proc', description='test descr')
        Action.objects.create(process=Process(id=1), title='test-action', description='test descr')
        Step.objects.create(action=Action(id=1), step_title='test step', 
                                                key_moment='test desc', key_moment_reason='test')
        

    def test_form_view_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/{process.slug}/action_creation/')
        self.assertEqual(response.status_code, 200)

    def test_form_view_uses_correct_template(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/{process.slug}/action_creation/')
        self.assertTemplateUsed('client_interface/action_creation.html')

    def test_redirect_is_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        title = 'test action'
        data = {
            'process': process,
            'title': title,
            'description': 'test descr',
            'step_title': 'test step',
            'key_moment': 'test key moment',
            'key_moment_reason': 'test key moment reason',
        }
        form = ActionCreationForm(data=data)
        response = c.post(f'/client/{course.slug}/{process.slug}/action_creation/', data=data)
        self.assertRedirects(response, f'/client/{course.slug}/{process.slug}/{slugify(title)}-2/action_added/')
        
    def test_action_added_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/{process.slug}/{action.slug}/action_added/')
        self.assertTemplateUsed('client_interface/action_added.html')

    def test_action_added_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.get(f'/client/{course.slug}/{process.slug}/{action.slug}/action_added/')
        showed_action = response.context['action']
        self.assertEqual(showed_action.process.course.title, course.title)
        self.assertEqual(showed_action.title, action.title)
       
class TestCourseShowingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test proc', description='test desk')

    def test_course_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/')
        self.assertEqual(response.status_code, 200)


    def test_course_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/')
        self.assertTemplateUsed('client_interface/course_showing.html')


    def test_course_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(course=course)
        response = c.get(f'/client/courses/{course.slug}/')
        showing_process = response.context['processes'][0]
        self.assertEqual(showing_process.title, process.title)
        self.assertEqual(showing_process.description, process.description)

class TestProcessShowingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test proc', description='test desk')
        Action.objects.create(process=Process(id=1), title='test action', description='test text')
        Action.objects.create(process=Process(id=1), title='test action', description='test text')

    def test_process_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_process_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/')
        self.assertTemplateUsed('client_interface/process_showing.html')

    def test_process_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        actions = process.action_set.all()
        action = Action.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/')
        first_showing_action = response.context['actions'][0]
        self.assertEqual(first_showing_action.title, action.title)
        self.assertEqual(first_showing_action.description, action.description)
        self.assertTrue(len(response.context['actions']) == 2)

class TestActionShowingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test proc', description='test desk')
        Action.objects.create(process=Process(id=1), title='test action', description='test text')
        Step.objects.create(action=Action(id=1), step_title='test step', 
                                                key_moment='test desc', key_moment_reason='test')
        Step.objects.create(action=Action(id=1), step_title='test step', 
                                                key_moment='test desc', key_moment_reason='test')

    def test_action_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/{action.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_action_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/{action.slug}/')
        self.assertTemplateUsed('client_interface/action_showing.html')

    def test_action_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        steps = Step.objects.filter(action=action)
        step = Step.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/{action.slug}/')
        first_showing_step = response.context['steps'][0]
        self.assertEqual(first_showing_step.step_title, step.step_title)
        self.assertEqual(first_showing_step.key_moment, step.key_moment)
        self.assertEqual(first_showing_step.key_moment_reason, step.key_moment_reason)
        self.assertTrue(len(response.context['steps']) == len(steps))

class TestCourseEditingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        

    def test_course_editing_url_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        response = c.get(f'/client/courses/{course.slug}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_course_editing_correct_template(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        response = c.get(f'/client/courses/{course.slug}/edit/')
        self.assertTemplateUsed('client_interface/course_edit.html')

    def test_course_editing_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        form = CourseCreationForm(instance=course)
        response = c.get(f'/client/courses/{course.slug}/edit/')
        showing_form = response.context['form']
        self.assertEqual(showing_form.instance.title, course.title)
        self.assertEqual(showing_form.instance.description, course.description)

    def test_course_editing_redirect_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        form = CourseCreationForm(instance=course)
        data = {
            'title': 'new title',
            'description': 'new descr',
        }
        response = c.post(f'/client/courses/{course.slug}/edit/', instance=course, data=data)
        self.assertRedirects(response, f'/client/courses/{course.slug}/')

class TestProcessEditingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test proc', description='test descr')

    def test_process_editing_url_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_process_editing_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/edit/')
        self.assertTemplateUsed('client_interface/process_edit.html')

    def test_process_editing_context_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/edit/')
        showing_form = response.context['form']
        self.assertEqual(showing_form.instance.title, process.title)
        self.assertEqual(showing_form.instance.description, process.description)

    def test_process_editing_redirect_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.filter(course=course).first()
        form = ProcessCreationForm(instance=process)
        title = 'new title'
        data = {
            'title': title,
            'description': 'new descr',
        }
        response = c.post(f'/client/courses/{course.slug}/{process.slug}/edit/', instance=process, data=data)
        self.assertRedirects(response, f'/client/courses/{course.slug}/')

class TestCourseDeletingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))

    def test_deleting_confirmation_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        response = c.get(f'/client/courses/{course.slug}/deletion/')
        self.assertEqual(response.status_code, 200)

    def test_deleting_confirmation_page_correct_template(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        response = c.get(f'/client/courses/{course.slug}/deletion/')
        self.assertTemplateUsed('client_interface/course_deletion.html')

    def test_deleting_course(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        response = c.post(f'/client/courses/{course.slug}/deletion/')
        self.assertFalse(Course.objects.filter(slug=course.slug).exists())

    def test_deleting_course_redirect_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        response = c.post(f'/client/courses/{course.slug}/deletion/')
        self.assertRedirects(response, '/client/')

class TestProcessDeletingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test process', description='test process descr' )

    def test_deleting_confirmation_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/deletion/')
        self.assertEqual(response.status_code, 200)

    def test_deleting_confirmatin_temlate_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/deletion/')
        self.assertTemplateUsed('client_interface/process_deletion.html')

    def test_deleting_process(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        response = c.post(f'/client/courses/{course.slug}/{process.slug}/deletion/')
        self.assertFalse(Process.objects.filter(slug=process.slug).exists())

    def test_deleting_process_redirect_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        response = c.post(f'/client/courses/{course.slug}/{process.slug}/deletion/')
        self.assertRedirects(response, f'/client/courses/{course.slug}/')
        
class TestActionDeletionView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Account.objects.create_user(email='test@twi.ru', username='test_user')
        cls.user.set_password('AaA12345')
        cls.user.save()
        Course.objects.create(title='test', description='test descr', owner=Account(id=1))
        Process.objects.create(course=Course(id=1), title='test process', description='test process descr' )
        Action.objects.create(process=Process(id=1), title='test-action', description='test descr')
        Step.objects.create(action=Action(id=1), step_title='test step', 
                                                key_moment='test desc', key_moment_reason='test')

    def test_deletion_confirmation_url_exists(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/{action.slug}/deletion/')
        self.assertEqual(response.status_code, 200)

    def test_deletion_confirmation_template_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.get(f'/client/courses/{course.slug}/{process.slug}/{action.slug}/deletion/')
        self.assertTemplateUsed('client_interface/action_deletion.html')
    
    def test_action_deleting(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.post(f'/client/courses/{course.slug}/{process.slug}/{action.slug}/deletion/')
        self.assertFalse(Action.objects.filter(slug=action.slug).exists())

    def test_deleting_action_redirect_correct(self):
        c = Client()
        c.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        course = Course.objects.get(owner=Account(id=1))
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = c.post(f'/client/courses/{course.slug}/{process.slug}/{action.slug}/deletion/')
        self.assertRedirects(response, f'/client/courses/{course.slug}/{process.slug}/')



    
