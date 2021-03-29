from django.test import TestCase, Client
from classroom_main import services
from user.forms import AvgRegisterForm
from django.contrib.auth import get_user_model
from user.models import User

class TestServices(TestCase):
    """ Test suite for 'classroom_main' services """
    def setUp(self):
        self.form = AvgRegisterForm(data={'email' : 'Testing@Email.com',
                                          'username' : 'Tester',
                                          'role' : 'AVERAGE',
                                          'first_name' : 'TesterName',
                                          'last_name' : 'TesterSurname',
                                          'password1' : 'TestPassword',
                                          'password2' : 'TestPassword'})

    def test_createNewUser(self):
        """ Method for testing the createNewUser method """
        # form.is_valid() must be run to give the form a 'cleaned_data' attribute
        if(self.form.is_valid()): 
            services.createNewUser(self.form)
        newUser = get_user_model().objects.filter(username__iexact="Tester")
        self.assertEqual(newUser[0].username, "Tester")
        self.assertIsInstance(newUser[0], User)
        