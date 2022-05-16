from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# import bcrypt
from hashlib import sha256
from .models import User

def index(request):
    return render(request, 'register/index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    hashed_password = sha256(request.POST['password'].encode()).hexdigest()
    user = User.objects.create(user_name=request.POST['user_name'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    if (User.objects.filter(email=request.POST['user_name']).exists()):
        user = User.objects.filter(email=request.POST['user_name'])[0]
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