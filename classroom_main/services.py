from django.contrib.auth import get_user_model

def createNewAcademicUser(form):
    # Retrieve and clean data from each form field
    email = form.cleaned_data.get('email')
    username = form.cleaned_data.get('username')
    role = form.cleaned_data.get('role')
    first_name = form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    password = form.cleaned_data.get('password1')

    # Create the user and save it to the database
    get_user_model().objects.create_user(email, username, role, first_name, last_name, password)

def createNewUser(form):
    # Retrieve and clean data from each form field
    email = form.cleaned_data.get('email')
    username = form.cleaned_data.get('username')
    role = "AVERAGE"
    first_name = form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    password = form.cleaned_data.get('password1')

    # Create the user and save it to the database
    get_user_model().objects.create_user(email, username, role, first_name, last_name, password)