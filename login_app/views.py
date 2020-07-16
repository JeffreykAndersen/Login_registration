from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

def home(request):
    return render(request, "main.html")

def register(request):
    if request.method =="POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print(key, value)
            return redirect('/')
        else:
            #this calls my UserManager class to create and register my user. Skinny views Fat Models.
            User.objects.register(request.POST)
            log_user = User.objects.last()
            request.session['user'] = f"{log_user.first_name} {log_user.last_name}"
            return redirect('/success')

def login(request):
    result = User.objects.authenticate(request.POST['log_email'], request.POST['log_password'])
    if result == False:
        messages.error(request, "Invalid Credentials")
        return redirect('/')
    if result == True:
        log_user = User.objects.get(email=request.POST['log_email'])
        request.session['user'] = f"{log_user.first_name} {log_user.last_name}"
        return redirect('/success')

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    return render(request, "loggedin.html",)

 
def logout(request):
    request.session.flush()
    print("session flushed")
    return redirect('/')




