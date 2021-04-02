from django.contrib.auth import get_user_model
from django.core.mail import send_mail

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


def send_new_email(feedback):
    """ Function for sending feedback email """
    send_mail("Feedback", feedback, "jordan.stenner@students.plymouth.ac.uk", ["jordan.stenner@students.plymouth.ac.uk"])