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
    school = models.ForeignKey(School, on_delete=models.CASCADE)                    # Foreign key for one-to-many relationship between School and Classes
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name

class Progress(models.Model):
    """ Model for a users Progress """
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)                    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    #grade = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    def __str__(self):
        return self.user.username + " | " + self.lesson.lesson_title

# Awards model for assigning awards to user accounts - Not within MVP
class Awards(models.Model):
    """ Model for user Awards """
    award_title = models.CharField(max_length=15)
    description = models.TextField(max_length=100)
    
    def __str__(self):
        return self.award_title
