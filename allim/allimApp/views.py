from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from .models import Teacher
import bcrypt

def index(request):
    return render(request,'index.html')

def Login_page(request):
    return render(request,'login.html')

def register_page(request):
    return render(request,'registration.html')

def reg_form(request):
    if request.method == "POST":
        errors = Teacher.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        models.Create_account(request.POST)
    return redirect('/')

def Login_form(request):
    email = models.Teacher.objects.filter(email=request.POST['email']).first()
            
    if bcrypt.checkpw(request.POST['password'].encode(),email.password.encode()):
        request.session['userid'] = email.id
        return redirect('/register')
    else:
        return redirect("/")

