from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from classroom_main.models import ComputingClass

ROLE_CHOICES = (
    ('TEACHER', 'Teacher'),
    ('STUDENT', 'Student'),
    ('AVERAGE', 'Average User'),
)

class UserManager(BaseUserManager):
    """ Class for UserManager - Use this to create users """
    # Method for creating a normal user
    def create_user(self, email, username, role, first_name, last_name, password=None):
        """ Function for creating standard users """
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        if not role:
            raise ValueError("Users must have a role")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            role = role,
            first_name = first_name,
            last_name = last_name
        )
        # If the role is TEACHER, they are staff
        if(role.upper() == "TEACHER"):
            user.is_staff = True

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method for creating a superuser/admin
    def create_superuser(self, email, username, role, first_name, last_name, password):
        """ Function for creating a superuser """
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            role = role,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Generic user model
class User(AbstractBaseUser):
    """ Custom User model """
    email        = models.EmailField(verbose_name="email", max_length=60, unique=True) 
    username     = models.CharField(max_length=30, unique=True)
    role         = models.CharField(max_length=12, choices=ROLE_CHOICES)
    first_name   = models.CharField(max_length=25)
    last_name    = models.CharField(max_length=30)
    #computing_class = models.ForeignKey(ComputingClass, on_delete=models.PROTECT) # Use for Student User
    #school = models.ForeignKey(School, on_delete=models.PROTECT) # Use for Teacher user
    # ADD AWARDS ONCE AWARDS COLLECTION IS CREATED
    date_joined  = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role', 'first_name', 'last_name',]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """ Function for checking admin permission """
        return self.is_admin

    def has_module_perms(self, app_label):
        """ Function for checking module permissions """
        return True
