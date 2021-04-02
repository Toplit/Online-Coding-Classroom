from django.test import TestCase, Client
from django.core import mail
from classroom_main import services
from user.forms import AvgRegisterForm, AcademicRegisterForm
from django.contrib.auth import get_user_model
from user.models import User

class TestServices(TestCase):
    """ Test suite for 'classroom_main' services """
    def setUp(self):
        self.formAvg = AvgRegisterForm(data={'email' : 'Testing@Email.com',
                                          'username' : 'Tester',
                                          'first_name' : 'TesterName',
                                          'last_name' : 'TesterSurname',
                                          'password1' : 'TestPassword',
                                          'password2' : 'TestPassword'})

        self.formAcademic = AcademicRegisterForm(data={'email' : 'Testing2@Email.com',
                                          'username' : 'Tester2',
                                          'role' : 'TEACHER',
                                          'first_name' : 'TesterName',
                                          'last_name' : 'TesterSurname',
                                          'password1' : 'TestPassword',
                                          'password2' : 'TestPassword'})
        pass

    def test_createNewUser(self):
        """ Method for testing the createNewUser method """
        # form.is_valid() must be run to give the form a 'cleaned_data' attribute
        if(self.formAvg.is_valid()): 
            services.createNewUser(self.formAvg)
        newUser = get_user_model().objects.filter(username__iexact="Tester")
        self.assertEqual(newUser[0].username, "Tester")
        self.assertEqual(newUser[0].role, "AVERAGE")
        self.assertFalse(newUser[0].is_staff)
        self.assertIsInstance(newUser[0], User)

    def test_createNewAcademicUser(self):
        """ Method for testing the createNewUser method """
        # form.is_valid() must be run to give the form a 'cleaned_data' attribute
        if(self.formAcademic.is_valid()): 
            services.createNewAcademicUser(self.formAcademic)
        newUser = get_user_model().objects.filter(username__iexact="Tester2")
        self.assertEqual(newUser[0].username, "Tester2")
        self.assertEqual(newUser[0].role, "TEACHER")
        self.assertTrue(newUser[0].is_staff)
        self.assertIsInstance(newUser[0], User)
        
    def test_send_new_mail(self):
        feedback = "Test email content"
        services.send_new_email(feedback)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Feedback")