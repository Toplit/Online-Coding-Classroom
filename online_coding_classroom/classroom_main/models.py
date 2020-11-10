from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class School(models.Model):
    """ Model for Schools """
    schoolName = models.TextField(max_length=40, unique=True)

class ComputingClass(models.Model):
    """ Model for Classes """
    classNum = models.CharField(max_length=15)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # MAY NOT WORK, COULD USE get_user_model()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    # SETTINGS.AUTH_USER_MODEL NOT WORKING
    # You can access all students for a Class object called X using: X.computingclass_set.objects.all()

    def __str__(self):
        return self.classNum


### LANGUAGE/LESSON MODELS - MAY BE MOVED INTO ITS OWN APP ###

class LanguageManager(models.Manager):
    """ Manager class for language methods """
    def get_lesson_count(self, lesson, language):
        """ Method for returning the lesson count for a particular language """
        count = lesson.objects.filter(language__languageName__iexact=language.languageName).count()
        return count

class Language(models.Model):
    """ Model for Programming Languages """
    languageName = models.CharField(max_length=15, unique=True)
    description = models.TextField(max_length=100)

    objects = LanguageManager()

class Lesson(models.Model):
    """ Model for Lessons """
    lessonTitle = models.CharField(max_length=20)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    lessonDescription = models.TextField(max_length=100)
    # Will have to change this data type to allow for formatting
    # Perhaps have all code on a txt file and have these files linked here
    # Maybe JSONField?
    lessonCode = models.TextField(max_length=300)

class LessonHint(models.Model):
    """ Model for Lesson Hints - One Lesson has many LessonHints """
    hintTitle = models.CharField(max_length=15)
    hintDescription = models.TextField(max_length=40)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class Progress(models.Model):
    """ Model for a users Progress """
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    grade = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

# Once implemented, create many to many relationship with User
class Awards(models.Model):
    """ Model for user Awards """
    awardTitle = models.CharField(max_length=15)
    description = models.TextField(max_length=100)
