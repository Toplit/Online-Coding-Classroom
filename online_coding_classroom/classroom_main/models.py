from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from lesson.models import Lesson

class School(models.Model):
    """ Model for Schools """
    school_name = models.CharField(max_length=40, unique=True)

class ComputingClass(models.Model):
    """ Model for Classes """
    class_name = models.CharField(max_length=15)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # MAY NOT WORK, COULD USE get_user_model()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # SETTINGS.AUTH_USER_MODEL NOT WORKING
    # You can access all students for a Class object called X using: X.computingclass_set.objects.all()

    def __str__(self):
        return self.class_name

class Progress(models.Model):
    """ Model for a users Progress """
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    grade = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    def __str__(self):
        return self.user

# Once implemented, create many to many relationship with User
class Awards(models.Model):
    """ Model for user Awards """
    award_title = models.CharField(max_length=15)
    description = models.TextField(max_length=100)
    
    def __str__(self):
        return self.award_title
