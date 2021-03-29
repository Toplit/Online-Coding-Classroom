from django.test import TestCase, Client
from classroom_main import services
from user.forms import AvgRegisterForm, AcademicRegisterForm
from django.contrib.auth import get_user_model
from user.models import User

class TestServices(TestCase):
    """ Test suite for testing the UserCreationForms """
    def setUp(self):
        self.averageForm = AvgRegisterForm(data={'email' : 'AverageTesting@Email.com',
                                          'username' : 'AverageTester',
                                          'role' : 'AVERAGE',
                                          'first_name' : 'TesterName',
                                          'last_name' : 'TesterSurname',
                                          'password1' : 'TestPassword',
                                          'password2' : 'TestPassword'})

        self.academicForm = AcademicRegisterForm(data={'email' : 'AcademicTesting@Email.com',
                                          'username' : 'AcademicTester',
                                          'role' : 'TEACHER',
                                          'first_name' : 'TesterName',
                                          'last_name' : 'TesterSurname',
                                          'password1' : 'TestPassword',
                                          'password2' : 'TestPassword'})

    def test_AvgRegisterForm(self):
        """ Method for testing that AvgRegisterForm is valid """
        self.assertTrue(self.averageForm.is_valid())

    def test_AcademicRegisterForm(self):
        """ Method for testing that AcademicRegisterForm is valid """
        self.assertTrue(self.academicForm.is_valid())
        