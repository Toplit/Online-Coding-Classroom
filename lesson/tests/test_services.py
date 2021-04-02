from lesson.models import ProgrammingEnvironment, Lesson, Language
from lesson import services
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
import json

class TestServices(TestCase):

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

    def test_get_value(self):
        """ Method to test the 'get_value' function """
        dictionary = {"TestKey":"TestValue"}
        result = services.get_value(dictionary, "TestKey")

        self.assertEqual(result, "TestValue")

    def test_get_lessons(self):
        """ Method to test the 'get_lessons' function """
        testLesson = services.get_lessons(self.language.language_name)

        self.assertEqual(testLesson[0].lesson_title, self.lesson.lesson_title)

    def test_get_languages(self):
        """ Method to test the 'get_languages' function """
        testLanguage = services.get_languages(self.environment.environment_name)

        self.assertEqual(testLanguage[0].language_name, self.language.language_name)

    def test_get_all_languages(self):
        """ Method to test the 'get_all_languages' function """
        testLanguages = services.get_all_languages()

        self.assertEqual(testLanguages[0].language_name, self.language.language_name)

    def test_language_lesson(self):
        """ Method to test the 'get_language_lesson' function """
        testLesson = services.get_language_lesson(self.language.language_name, self.lesson.lesson_title)

        self.assertEqual(testLesson[0].lesson_title, self.lesson.lesson_title)

    def test_get_single_language(self):
        """ Method to test the 'get_single_language' function """
        testLanguage = services.get_single_language(self.language.language_name)

        self.assertEqual(testLanguage[0].language_name, self.language.language_name)

    def test_compile_javascript_code(self):
        """ Method to test the 'compile_javascript_code' method """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=function%20variable_exercise()%7B%0A%20%20%2F%2FWrite%20variable%20here%0A%09return%20%22Test%22%0A%20%20%2F%2FReturn%20the%20variable%20here%0A%7D&language=javascript')
        data = services.compile_javascript_code(request)

        data = json.loads(data.content)
        self.assertEqual(data['output'], "Test")

    def test_compile_python_code(self):
        """ Method to test the 'compile_python_code' method """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=def%20variables_exercise()%3A%0A%20%20%20%20%23%20Write%20variable%20here%20%0A%09return%20%22Test%22%0A%20%20%20%20%23%20Return%20the%20variable&language=python')
        data = services.compile_python_code(request)

        data = json.loads(data.content)
        self.assertEqual(data['output'], "Test")

    def test_compile_web_code_valid(self):
        """ Method to test the 'compile_code' function for HTML & CSS with valid structure """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=%3Chtml%3E%0A%3Chead%3E%0A%3C%2Fhead%3E%0A%3Cbody%3E%0A%3C!--%20Create%20a%20H1%20tag%20here%20with%20the%20text%20%22Hello%20World!%22%20in%20--%3E%0A%20%20%3Ch1%3ETest%3C%2Fh1%3E%0A%3C%2Fbody%3E%0A%3C%2Fhtml%3E&language=html%20and%20css')
        data = services.compile_web_code(request)

        data = json.loads(data.content)
        self.assertInHTML(r'<h1>Test</h1>', data['HTML'])

    def test_compile_web_code_invalid(self):
        """ Method to test the 'compile_code' function for HTML & CSS with invalid structure """
        factory = RequestFactory()
        request = factory.get(r'/get_code/?untrustedCode=%3Chead%3E%0A%3C%2Fhead%3E%0A%3Cbody%3E%0A%3C!--%20Create%20a%20H1%20tag%20here%20with%20the%20text%20%22Hello%20World!%22%20in%20--%3E%0A%20%20%3Ch1%3ETest%3C%2Fh1%3E%0A%3C%2Fbody%3E&language=html%20and%20css')
        data = services.compile_web_code(request)

        data = json.loads(data.content)
        self.assertInHTML("You forgot to add core HTML structures such as <html>, <body> or <head>!", data['output'])
    