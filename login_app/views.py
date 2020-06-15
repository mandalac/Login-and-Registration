from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    errors = User.objects.registrationValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashpw)
        messages.info(request, 'The account is created, plese LogIn')
        return redirect('/')

def login (request):
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, 'Invalid email adress')
        return redirect('/')
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, 'Invalid password')
        return redirect('/')
    else:
        request.session['user_firstName'] = user.first_name
        return redirect('/succes')
    return redirect('/')

def succes(request):
    return render(request, 'succes.html')    

def logout(request):
    del request.session['user_firstName']
    return redirect('/')
    