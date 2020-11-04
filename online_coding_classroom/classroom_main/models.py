from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.
class Class(models.Model):
    """ Model for classes """
    classNum = models.TextField(max_length=15)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL)
    # MAY NEED ADMINMODEL INLINE FOR THIS

    def __str__(self):
        return self.classNum
