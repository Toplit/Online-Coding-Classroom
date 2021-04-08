from django.test import TestCase, Client
from classroom_main import services
from user.forms import AvgRegisterForm, AcademicRegisterForm, PasswordResetForm
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

        self.passwordResetFormValid = PasswordResetForm(data={'old_password' : 'oldpassword',
                                                              'new_password' : 'newpassword',
                                                              'confirm_password' : 'newpassword' })

        self.passwordResetFormInvalid = PasswordResetForm(data={'old_password' : 'oldpassword',
                                                              'new_password' : 'newpassword',
                                                              'confirm_password' : 'differentpassword' })

    def test_AvgRegisterForm(self):
        """ Method for testing that AvgRegisterForm is valid """
        self.assertTrue(self.averageForm.is_valid())

    def test_AcademicRegisterForm(self):
        """ Method for testing that AcademicRegisterForm is valid """
        self.assertTrue(self.academicForm.is_valid())

    def test_PasswordResetForm_valid(self):
        """ Method for testing the PasswordResetForm with matching new passwords """
        self.assertTrue(self.passwordResetFormValid.is_valid())

    def test_PasswordResetForm_invalid(self):
        """ Method for testing the PasswordResetForm with non-matching new passwords """
        self.assertFalse(self.passwordResetFormInvalid.is_valid())