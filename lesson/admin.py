from django.contrib import admin
from lesson.models import ProgrammingEnvironment, Language, Lesson, LessonHint

# list_display - Show these fields for each model on the Admin site
# search_fields - Allow searching in these fields

# Register models for the Admin site
class ProgrammingEnvironmentAdmin(admin.ModelAdmin):
    """ Model for the Admin page """
    list_display = ('environment_name', 'description')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class LanguageAdmin(admin.ModelAdmin):
    """ Model for the Admin page """
    list_display = ('language_name', 'description', 'environment')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class LessonAdmin(admin.ModelAdmin):
    """ Model for the Admin page """
    list_display = ('lesson_number', 'lesson_title', 'language', 'lesson_description')
    search_fields = ('language', 'lesson_title')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class LessonHintAdmin(admin.ModelAdmin):
    """ Model for the Admin page """
    list_display = ('hint_title', 'lesson', 'hint_description')
    search_fields = ('hint_title','lesson')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ProgrammingEnvironment, ProgrammingEnvironmentAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonHint, LessonHintAdmin)