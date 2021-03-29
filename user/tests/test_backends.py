from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import User, UserManager
from user.backends import CaseInsensitiveModelBackend

class TestBackends(TestCase):

    def setUp(self):
        """ Method to set up the client and database content for Users """
        self.client = Client()
        self.username = "Testing@Email.com"
        self.password = "TestingPassword"
        self.user = get_user_model().objects.create_user("Testing@Email.com", "Test", "TEACHER", "Tester", "Testing", "TestingPassword")
        pass

    def test_authenticate_valid(self):
        """ Method for testing that authenticate returns user when password is valid """
        factory = RequestFactory()
        request = '/'
        testUser = CaseInsensitiveModelBackend().authenticate(request, self.username, self.password)

        self.assertEqual(testUser.username, self.user.username)

    def test_authenticate_invalid(self):
        """ Method for testing that authenticate returns None when password is invalid """
        factory = RequestFactory()
        request = '/'
        testUser = CaseInsensitiveModelBackend().authenticate(request, "WrongUser", "WrongPass")

        self.assertIsNone(testUser)
