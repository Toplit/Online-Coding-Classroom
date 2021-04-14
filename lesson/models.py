from django.db import models

# Relationship of models:
# ProgrammingEnvironment has many Languages
# Languages have many lessons
# Lessons have many lesson hints

class LanguageManager(models.Manager):
    """ Manager class for language methods """
    def get_lesson_count(self, lesson, language):
        """ Method for returning the lesson count for a particular language """
        count = lesson.objects.filter(language__language_name__iexact=language.language_name).count()
        return count

class ProgrammingEnvironment(models.Model):
    """ Model for Programming Types """
    environment_name = models.CharField(max_length=30, unique=True, primary_key=True)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.environment_name

class Language(models.Model):
    """ Model for Programming Environments """
    language_name = models.CharField(max_length=15, unique=True)
    description = models.TextField(max_length=100)

    environment = models.ForeignKey(ProgrammingEnvironment, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.language_name

class Lesson(models.Model):
    """ Model for Lessons """
    lesson_title = models.CharField(max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    lesson_summary = models.TextField()
    lesson_description = models.TextField() # Used for the lesson exercise description
    lesson_content = models.TextField()     # Used for the lesson topic explanation
    lesson_code = models.TextField()        # Used for the lesson exercise code
    check_result = models.TextField()       # Used for the JavaScript check input code 
    lesson_number = models.IntegerField()

    def __str__(self):
        return self.language.language_name +": "+self.lesson_title

class LessonHint(models.Model):
    """ Model for Lesson Hints - One Lesson has many LessonHints """
    hint_title = models.CharField(max_length=30)
    hint_description = models.TextField(max_length=300)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.hint_title