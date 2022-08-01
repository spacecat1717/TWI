from django.test import TestCase
from courses.models import Course, Action, Step


class CoursesListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        total_courses = 5
        for num in range(total_courses):
            Course.objects.create(title='test', description='test descr', 
                    cover='/media/courses/covers/static/20_Lazy_Cats_That_Will_Make_You_LOL.jpg')

    def test_view_url_exists(self):
        response = self.client.get('/courses_list/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/courses_list/')
        self.assertTemplateUsed(response, 'courses/courses_list.html')

    def test_context_is_correct(self):
        response = self.client.get('/courses_list/')
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
        total_actions = 3
        for i in range(total_actions +1):
            Action.objects.create(course=Course(id=1), title='test action', 
                                cover='media/courses/actions/covers/static/1583861548.6278.jpg')
        
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
        actions = Action.objects.all()
        action = Action.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/')
        first_course_action = response.context['course_actions'][0]
        self.assertEquals(first_course_action.title, action.title)
        self.assertEquals(first_course_action.cover, action.cover)
        self.assertTrue(len(response.context['course_actions']) == len(actions))

    """ TODO: надо найти способ проверять ссылки на страницах (парсинг)
    def test_link_to_action_working(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(id=1)
        get = self.client.get(f'/courses/{course.slug}/')
        response = get.html
        page_content = BeautifulSoup(response.text, 'lxml')
        link_raw = page_content.find('a', class_='link')
        link = link_raw.text
        print('parsed link', link)
        redirect_response = self.client.get(link)
        self.assertEqual(redirect_response.status_code, 200)
        """

class ActionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', 
                    cover='/media/courses/covers/static/20_Lazy_Cats_That_Will_Make_You_LOL.jpg')
        Action.objects.create(course=Course(id=1), title='test action', 
                                cover='media/courses/actions/covers/static/1583861548.6278.jpg')
        Step.objects.create(action=Action(id=1), title='test step', description='test desc', 
                                                                    main_text='test text')

    def test_view_url_exists(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course)
        response = self.client.get(f'/courses/{course.slug}/{action.slug}/')
        return self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course)
        self.assertTemplateUsed('courses/action.html') 

    def test_context_is_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course) 
        steps = Step.objects.all()
        step = Step.objects.get(id=1)
        response = self.client.get(f'/courses/{course.slug}/{action.slug}/')
        first_action_step = response.context['steps'][0]
        self.assertEqual(first_action_step.title, step.title)
        self.assertEqual(first_action_step.description, step.description)
        self.assertEqual(first_action_step.main_text, step.main_text)
        #TODO: add photos test
        self.assertTrue(len(response.context['steps']) == len(steps)) 

class StepViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(title='test', description='test descr', 
                    cover='/media/courses/covers/static/20_Lazy_Cats_That_Will_Make_You_LOL.jpg')
        Action.objects.create(course=Course(id=1), title='test action', 
                                cover='media/courses/actions/covers/static/1583861548.6278.jpg')
        Step.objects.create(action=Action(id=1), title='test step', description='test desc', 
                                                                    main_text='test text')

    def test_view_url_exists(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course)
        step = Step.objects.get(action=action)
        response = self.client.get(f'/courses/{course.slug}/{action.slug}/{step.slug}/')
        return self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course)
        step = Step.objects.get(action=action)
        self.assertTemplateUsed('courses/step.html')
    
    def test_context_is_correct(self):
        course = Course.objects.get(id=1)
        action = Action.objects.get(course=course)
        step = Step.objects.get(action=action)
        response = self.client.get(f'/courses/{course.slug}/{action.slug}/{step.slug}/')
        step_showed = response.context['step']
        self.assertEqual(step_showed.title, step.title)
        self.assertEqual(step_showed.description, step.description)
        self.assertEqual(step_showed.main_text, step.main_text)
        

        
               
