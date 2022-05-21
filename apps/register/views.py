from distutils.log import error
import email
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from hashlib import sha256
from .models import User
import re

def mob_number_validator(mob_number):
    mob_number_messages = []
    if len(mob_number) != 10:
        mob_number_messages.append("Invalid Mobile Number! Mobile number has to be 10 digits long.")
    return mob_number_messages

def email_validator(email):
    email_messages = []
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        email_messages.append("Invalid Email! Email must have an @ symbol followed by the domain.")
    return email_messages

def password_validator(password):
    password_messages = []
    valid = True

    if len(password) < 12:
        password_messages.append("Password must be greater than 12 characters")
    
    if not any(char.isdigit() for char in password):
        password_messages.append("Password must contain atleast 1 number")

    if not any(char.isupper() for char in password):
        password_messages.append("Password must contain alteast 1 upper case character")

    if not any(char.islower() for char in password):
        password_messages.append("Password must contain alteast 1 lower case character")

    if not any(char in ['$', '@', '#', '!', '%'] for char in password):
        password_messages.append("Password must contain alteast 1 special character")

    return password_messages

def confirm_password_validator(password, confirm_password):
    confirm_password_messages = []
    if confirm_password != password:
        confirm_password_messages.append("Password & Confirm Password must match.")
    return confirm_password_messages



def index(request):
    return render(request, 'register/index.html')

def register(request):
    mob_number_messages = mob_number_validator(request.POST['mob_number'])
    email_messages = email_validator(request.POST['email'])
    password_messages = password_validator(request.POST['password'])

    error_messages = {}
    valid = True

    if len(mob_number_messages) > 0:
        valid = False
        error_messages['mob_number_messages'] = mob_number_messages[0]

    if len(email_messages) > 0:
        valid = False
        error_messages['email_messages'] = email_messages[0]

    if len(password_messages) > 0:
        valid = False
        error_messages['password_messages'] = password_messages
    
    if len(password_messages) == 0:
        confirm_password_messages = confirm_password_validator(request.POST['password'], request.POST['confirm_password'])
        if len(confirm_password_messages) > 0:
            valid = False
            error_messages['confirm_password_messages'] = confirm_password_messages[0]

    if valid:
        hashed_password = sha256(request.POST['password'].encode()).hexdigest()
        user = User.objects.create(user_name=request.POST['user_name'], password=hashed_password, email=request.POST['email'], mob_number=request.POST['mob_number'], address=request.POST['address'])
        user.save()
        request.session['id'] = user.id
        return redirect('/success')
    
    else:
        # messages = error_messages
        return render(request, 'register/index.html', error_messages)

def login(request):
    if (User.objects.filter(user_name=request.POST['user_name']).exists()):
        user = User.objects.filter(user_name=request.POST['user_name'])[0]

        if ((sha256(request.POST['login_password'].encode()).hexdigest()).encode() == user.password.encode()):
            request.session['id'] = user.id
            return redirect('/success')
    return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'register/success.html', context)