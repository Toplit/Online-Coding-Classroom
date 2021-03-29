from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import User, UserManager

class TestModels(TestCase):
    def test_create_user_average(self):
        """ Method to test the create_user method for average users """
        self.genericUser = get_user_model().objects.create_user("Testing@Email.com", "Test", "AVERAGE", "Tester", "Testing", "TestingPassword")

        self.assertEqual(self.genericUser.role, "AVERAGE")
        self.assertFalse(self.genericUser.is_staff)
        self.assertFalse(self.genericUser.is_admin)
        self.assertFalse(self.genericUser.is_superuser)
        self.assertFalse(self.genericUser.has_perm("test_perm"))  # Users do not yet have permissions, but should only be true for superusers currently

    def test_create_user_academic(self):
        """ Method to test the create_user method for academic users """
        self.genericUser = get_user_model().objects.create_user("Teacher@Email.com", "Teacher", "TEACHER", "Teacher", "TestingTeacher", "TestingPassword")

        self.assertEqual(self.genericUser.role, "TEACHER")
        self.assertTrue(self.genericUser.is_staff)
        self.assertFalse(self.genericUser.is_admin)
        self.assertFalse(self.genericUser.is_superuser)
        self.assertFalse(self.genericUser.has_perm("test_perm"))  # Users do not yet have permissions, but should only be true for superusers currently

    def test_create_superuser(self):
        """ Method to test the create_superuser method for superusers """
        self.superUser = get_user_model().objects.create_superuser("Admin@Email.com", "Admin", "AVERAGE", "Admin", "AdminSurname", "TestingPassword")

        self.assertEqual(self.superUser.role, "AVERAGE")
        self.assertTrue(self.superUser.is_staff)
        self.assertTrue(self.superUser.is_admin)
        self.assertTrue(self.superUser.is_superuser)
        self.assertTrue(self.superUser.has_perm("test_perm"))  # Always true for superusers

    def test_has_perm(self):
        """ Method to test the permissions for each type of user """
        self.genericUser = get_user_model().objects.create_user("Testing@Email.com", "Test", "AVERAGE", "Tester", "Testing", "TestingPassword")
        self.superUser = get_user_model().objects.create_superuser("Admin@Email.com", "Admin", "AVERAGE", "Admin", "AdminSurname", "TestingPassword")

        self.assertFalse(self.genericUser.has_perm("test_perm"))
        self.assertTrue(self.superUser.has_perm("test_perm"))

    ### Medule permissions not yet implemented
    # def test_module_perms(self):
    #     self.genericUser = get_user_model().objects.create_user("Testing@Email.com", "Test", "AVERAGE", "Tester", "Testing", "TestingPassword")
    #     self.superUser = get_user_model().objects.create_superuser("Admin@Email.com", "Admin", "AVERAGE", "Admin", "AdminSurname", "TestingPassword")

    #     self.assertTrue(self.superUser.has_module_perms("lesson"))
    #     self.assertFalse(self.genericUser.has_module_perms("lesson"))