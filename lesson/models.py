from django.db import models

### LANGUAGE/LESSON MODELS - MAY BE MOVED INTO ITS OWN APP ###

class LanguageManager(models.Manager):
    """ Manager class for language methods """
    def get_lesson_count(self, lesson, language):
        """ Method for returning the lesson count for a particular language """
        count = lesson.objects.filter(language__language_name__iexact=language.language_name).count()
        return count

class Language(models.Model):
    """ Model for Programming Languages """
    language_name = models.CharField(max_length=15, unique=True)
    description = models.TextField(max_length=100)

    #objects = LanguageManager() ## remove this

    def __str__(self):
        return self.language_name

class Lesson(models.Model):
    """ Model for Lessons """
    lesson_title = models.CharField(max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    lesson_description = models.TextField()
    lesson_content = models.TextField()
    lesson_code = models.TextField()
    check_result = models.TextField()
    compile_url = models.CharField(max_length=50)
    lesson_number = models.IntegerField()

    def __str__(self):
        return self.lesson_title

class LessonHint(models.Model):
    """ Model for Lesson Hints - One Lesson has many LessonHints """
    hint_title = models.CharField(max_length=15)
    hint_description = models.TextField(max_length=40)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.hint_title