from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User

# Register your models here.
class TheUserAdmin(UserAdmin):
    """ Model for the Admin page """
    list_display = ('email', 'role', 'first_name', 'last_name', 'date_joined', 
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, TheUserAdmin)
