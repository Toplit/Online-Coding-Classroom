from django.contrib import admin
from lesson.models import Language, Lesson, LessonHint

# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    """ Model for the Admin page """
    list_display = ('language_name', 'description')
    #readonly_fields = ('id', 'language_name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class LessonAdmin(admin.ModelAdmin):
    """ Model for the Admin page """
    list_display = ('lesson_title', 'language', 'lesson_description')
    #readonly_fields = ('language', 'lesson_title', 'lesson_description')
    search_fields = ('language', 'lesson_title')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class LessonHintAdmin(admin.ModelAdmin):
    """ Model for the Admin page """
    list_display = ('hint_title', 'lesson', 'hint_description')
    #readonly_fields = ('hint_title', 'lesson', 'hint_description')
    search_fields = ('hint_title','lesson')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Language, LanguageAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonHint, LessonHintAdmin)

#admin.site.register(Lesson)
#admin.site.register(LessonHint)
#admin.site.register(Language)