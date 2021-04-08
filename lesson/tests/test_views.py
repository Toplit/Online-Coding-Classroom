from django.contrib.auth import get_user_model
from lesson.models import ProgrammingEnvironment, Language, Lesson
from classroom_main.models import Progress
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from lesson.views import compile_code
import json

class TestViews(TestCase):
    """ Test suite for 'lesson' views """
    def setUp(self):
        """ Method to set up the client and database content for Users, Programming Environments, Languages and Lessons """
        self.client = Client()
        self.username = "Testing@Email.com"
        self.password = "TestingPassword"
        self.user = get_user_model().objects.create_user("Testing@Email.com", "Test", "TEACHER", "Tester", "Testing", "TestingPassword")

        self.saveLessonsToDB()
        pass

    def saveLessonsToDB(self):
        """ Method to create Programming Environment, Language and Lesson for the test database """
        self.environment = ProgrammingEnvironment(environment_name="Web Applications", description="Test Description")
        self.environment.save()
        
        self.language = Language(language_name="JavaScript", description="Test Description", environment=self.environment)
        self.language.save()

        self.lesson = Lesson(language=self.language, lesson_title="Variables", lesson_description="Test Description",
                                      lesson_content="Test content", check_result="function check_result(result)\{\}", lesson_number=1,
                                      lesson_code="""
function variable_exercise(){
  //Write variable here
	
  //Return the variable here
}""")
        self.lesson.save()

    def login_client(self):
        """ Method for logging in the client """
        self.client.login(username=self.username, password=self.password)

    def test_select_env_notloggedin(self):
        """ Method to test requesting the select environments page when not logged in """
        response = self.client.get(reverse("lesson-select-env"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/login.html")

    def test_select_env_loggedin(self):
        """ Method to test requesting the select environments page when logged in """
        self.login_client()
        response = self.client.get(reverse("lesson-select-env"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lesson/select_env.html")

    def test_select_language_notloggedin(self):
        """ Method to test requesting the select language page when not logged in """
        response = self.client.get(reverse("lesson-select-language", kwargs={'environmentName':self.environment.environment_name}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/login.html")

    def test_select_language_loggedin(self):
        """ Method to test requesting the select language page when logged in """
        self.login_client()
        response = self.client.get(reverse("lesson-select-language", kwargs={'environmentName':self.environment.environment_name}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lesson/select_language.html")

    def test_select_lesson_notloggedin(self):
        """ Method to test requesting the select lesson page when not logged in """
        response = self.client.get(reverse("lesson-select-lesson", kwargs={'languageTitle':self.language.language_name}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/login.html")

    def test_select_lesson_loggedin(self):
        """ Method to test requesting the select lesson page when logged in """
        self.login_client()
        response = self.client.get(reverse("lesson-select-lesson", kwargs={'languageTitle':self.language.language_name}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lesson/select_lesson.html")

    def test_lesson_loggedin(self):
        """ Method to test requesting the lesson page when logged in """
        self.login_client()
        response = self.client.get(reverse("lesson-lesson-specific", kwargs={'languageTitle':self.language.language_name, 'lessonTitle':self.lesson.lesson_title}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lesson/lesson_base.html")
        self.assertInHTML(self.lesson.lesson_code, response.content.decode())

    def test_next_lesson(self):
        """ Method used to test the 'next_lesson' function """
        nextLesson = Lesson(language=self.language, lesson_title="Conditionals", lesson_description="Test Description",
                                lesson_content="Test content", check_result="function check_result(result)\{\}", lesson_number=2,
                                lesson_code="""test""")
        nextLesson.save()
        self.login_client()
        response = self.client.get(reverse("lesson-next-lesson", kwargs={"languageTitle": self.language.language_name, "currentLessonTitle":self.lesson.lesson_title, "nextLessonTitle": nextLesson.lesson_title}), follow=True)

        newProgress = Progress.objects.filter(lesson__lesson_title=self.lesson.lesson_title)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lesson/lesson_base.html")
        self.assertInHTML(nextLesson.lesson_title, response.content.decode())
        self.assertIsNotNone(newProgress)

    def test_language_complete(self):
        self.login_client()
        response = self.client.get(reverse("lesson-language-complete", kwargs={'languageTitle':self.language.language_name, 'lessonTitle':self.lesson.lesson_title}))

        newProgress = Progress.objects.filter(lesson__lesson_title=self.lesson.lesson_title)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lesson/language_complete.html")
        self.assertInHTML("Language Complete!", response.content.decode())
        self.assertIsNotNone(newProgress)

    def test_compile_code_JS(self):
        """ Method to test the 'compile_code' function for JavaScript """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=function%20variable_exercise()%7B%0A%20%20%2F%2FWrite%20variable%20here%0A%09return%20%22Test%22%0A%20%20%2F%2FReturn%20the%20variable%20here%0A%7D&language=javascript')
        data = compile_code(request)

        data = json.loads(data.content)
        self.assertEqual(data['output'], "Test")

    def test_compile_code_python(self):
        """ Method to test the 'compile_code' function for Python """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=def%20variables_exercise()%3A%0A%20%20%20%20%23%20Write%20variable%20here%20%0A%09return%20%22Test%22%0A%20%20%20%20%23%20Return%20the%20variable&language=python')
        data = compile_code(request)

        data = json.loads(data.content)
        self.assertEqual(data['output'], "Test")

    def test_compile_code_htmlcss_valid(self):
        """ Method to test the 'compile_code' function for HTML & CSS """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=%3Chtml%3E%0A%3Chead%3E%0A%3C%2Fhead%3E%0A%3Cbody%3E%0A%3C!--%20Create%20a%20H1%20tag%20here%20with%20the%20text%20%22Hello%20World!%22%20in%20--%3E%0A%20%20%3Ch1%3ETest%3C%2Fh1%3E%0A%3C%2Fbody%3E%0A%3C%2Fhtml%3E&language=html%20and%20css')
        data = compile_code(request)

        data = json.loads(data.content)
        self.assertInHTML(r'<h1>Test</h1>', data['HTML'])

    def test_compile_code_htmlcss_invalid(self):
        """ Method to test the 'compile_code' function for HTML & CSS """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=%3Chead%3E%0A%3C%2Fhead%3E%0A%3Cbody%3E%0A%3C!--%20Create%20a%20H1%20tag%20here%20with%20the%20text%20%22Hello%20World!%22%20in%20--%3E%0A%20%20%3Ch1%3ETest%3C%2Fh1%3E%0A%3C%2Fbody%3E&language=html%20and%20css')
        data = compile_code(request)

        data = json.loads(data.content)
        self.assertInHTML("You forgot to add core HTML structures such as <html>, <body> or <head>!", data['output'])