from django.contrib.auth import get_user_model
from user.models import User
from lesson.models import Language, ProgrammingEnvironment
from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):
    """ Test suite for 'classroom_main' views """
    def setUp(self):
        self.client = Client()
        self.username = "Testing@Email.com"
        self.password = "TestingPassword"
        self.user = get_user_model().objects.create_user("Testing@Email.com", "Test", "TEACHER", "Tester", "Testing", "TestingPassword")
        self.environment = ProgrammingEnvironment(environment_name="Web Applications", description="Test Description")
        self.environment.save()
        self.language = Language(language_name="JavaScript", description="Test Description", environment=self.environment)
        self.language.save()
        pass

    def login_client(self):
        """ Method for logging in the client """
        self.client.login(username=self.username, password=self.password)

    def test_home_notloggedin(self):
        """ Method to test requesting the home page when not logged in """
        response = self.client.get(reverse("classroom-home"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/login.html")

    def test_home_loggedin(self):
        """ Method to test requesting the home page when logged in """
        self.login_client()
        response = self.client.get(reverse("classroom-home"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/home.html")

    def test_my_account_notloggedin(self):
        """ Method to test requesting the 'My Account' page when not logged in """
        response = self.client.get(reverse("classroom-my-account"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/login.html")

    def test_my_account_loggedin(self):
        """ Method to test requesting the 'My Account' page when logged in """
        self.login_client()
        response = self.client.get(reverse("classroom-my-account"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/my_account.html")

    def test_performance_analysis_notloggedin(self):
        """ Method to test requesting the 'Performance Analysis' page when not logged in """
        response = self.client.get(reverse("classroom-performance-analysis"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/login.html")

    def test_performance_analysis_loggedin(self):
        """ Method to test requesting the 'Performance Analysis' page when logged in """
        self.login_client()
        response = self.client.get(reverse("classroom-performance-analysis"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classroom_main/performance_analysis.html")
    
    def test_login_valid(self):
        """ Method to logging in with valid credentials """
        response = self.client.post(reverse("login"), {"username" : self.username, "password" : self.password}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertTemplateUsed(response, "classroom_main/home.html")

    def test_login_invalid(self):
        """ Method to logging in with invalid credentials """
        response = self.client.post(reverse("login"), {"username" : "WrongUser", "password" : "WrongPass"}, follow=True)
        self.assertTemplateUsed(response, "classroom_main/login.html")

    def test_logout(self):
        """ Method to test the logout functionality """
        self.login_client()
        response = self.client.get(reverse("classroom-home"), follow=True)
        self.assertEqual(response.context['user'], self.user)
        response = self.client.get(reverse("logout"), follow=True)
        self.assertNotEqual(response.context['user'], self.user)
        self.assertTemplateUsed(response, "classroom_main/logout.html")

    def test_create_account(self):
        """ Method to test the 'create_account' method """
        response = self.client.post(reverse("classroom-create-account", kwargs={"role" : "average"}), {"email" : "test@testing.com",
                                                                                                    "username" : "TestingUser",
                                                                                                    "first_name" : "Tester2",
                                                                                                    "last_name" : "Tester2",
                                                                                                    "role" : "AVERAGE",
                                                                                                    "password1" : "TestingPassword",
                                                                                                    "password2" : "TestingPassword"}, follow=True)
        self.assertEqual(response.status_code, 200)
        newUser = get_user_model().objects.filter(username__iexact="TestingUser")
        self.assertEqual(newUser[0].username, "TestingUser")
        self.assertIsInstance(newUser[0], User)
        