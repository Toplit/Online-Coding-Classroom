from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User

# list_display - Show these fields for each model on the Admin site
# search_fields - Allow searching in these fields
# readonly_fields - Do not allow modification of these fields
# add_fieldsets - Add these fields to the creation form in Admin

class TheUserAdmin(UserAdmin):
    """ Model for the Admin page """
    list_display = ('email', 'role', 'first_name', 'last_name', 'date_joined', 
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'role', 'first_name', 'last_name', 'password1', 'password2'),
            }),
        )
admin.site.register(User, TheUserAdmin)
