from django.test import TestCase
from courses.models import Course, Action, Step, Process


class CoursesListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        total_courses = 5
        for num in range(total_courses):
            Course.objects.create(title='test', description='test descr', 
                    cover='/media/courses/covers/static/20_Lazy_Cats_That_Will_Make_You_LOL.jpg')

    def test_view_url_exists(self):
        response = self.client.get('/courses/courses_list/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/courses/courses_list/')
        self.assertTemplateUsed(response, 'courses/courses_list.html')

    def test_context_is_correct(self):
        response = self.client.get('/courses/courses_list/')
        courses = Course.objects.all()
        first_object = response.context['courses'][0]
        for course in courses:    
            self.assertEqual(first_object.title, course.title)
            self.assertEqual(first_object.description, course.description)
            self.assertEqual(first_object.cover, course.cover)
        self.assertTrue(len(response.context['courses']) == 5)


class CourseViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', 
                    cover='/media/courses/covers/static/20_Lazy_Cats_That_Will_Make_You_LOL.jpg')
        total_processes = 3
        for i in range(total_processes +1):
            Process.objects.create(course=Course(id=1), title='test title', description='test descr')
        
    def test_view_url_exists(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        course = Course.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/')
        self.assertTemplateUsed(response, 'courses/course.html')

    def test_context_is_correct(self):
        course = Course.objects.get(id=1)
        processes = Process.objects.all()
        process = Process.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/')
        first_course_process = response.context['processes'][0]
        self.assertEquals(first_course_process.title, process.title)
        self.assertEquals(first_course_process.cover, process.cover)
        self.assertTrue(len(response.context['processes']) == len(processes))

class ProcessViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', 
                    cover='/media/courses/covers/static/20_Lazy_Cats_That_Will_Make_You_LOL.jpg')
        Process.objects.create(course=Course(id=1), title='test title', description='test descr')
        Action.objects.create(process=Process(id=1), title='test action')

    def test_view_url_exists(self):
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/{process.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/{process.slug}/')
        self.assertTemplateUsed('courses/process.html')

    def test_context_is_correct(self):
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/{process.slug}/')
        first_showing_action = response.context['actions'][0]
        self.assertEqual(first_showing_action.title, action.title)
        self.assertEqual(first_showing_action.main_text, action.main_text)
        self.assertTrue(len(response.context['actions']) == 1)
        

class ActionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', 
                    cover='/media/courses/covers/static/20_Lazy_Cats_That_Will_Make_You_LOL.jpg')
        Process.objects.create(course=Course(id=1), title='test title', description='test descr')
        Action.objects.create(process=Process(id=1), title='test action')
        Step.objects.create(action=Action(id=1), title='test step', description='test descr')

    def test_view_url_exists(self):
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/{process.slug}/{action.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/{process.slug}/{action.slug}/')
        self.assertTemplateUsed('courses/action.html')

    def test_context_is_correct(self):
        course = Course.objects.get(id=1)
        process = Process.objects.get(id=1)
        action = Action.objects.get(id=1)
        step = Step.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/{process.slug}/{action.slug}/')
        first_showing_step = response.context['steps'][0]
        showing_action = response.context['action']
        self.assertEqual(first_showing_step.title, step.title)
        self.assertEqual(first_showing_step.description, step.description)
        self.assertEqual(showing_action.main_text, action.main_text)
        self.assertTrue(len(response.context['steps']) == 1)

    

        
               
