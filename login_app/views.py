from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
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
            request.session['id'] = log_user.id
            return redirect('/success')

def login(request):
    result = User.objects.authenticate(request.POST['log_email'], request.POST['log_password'])
    if result == False:
        messages.error(request, "Invalid Credentials")
        return redirect('/')
    if result == True:
        log_user = User.objects.get(email=request.POST['log_email'])
        request.session['user'] = f"{log_user.first_name} {log_user.last_name}"
        request.session['id'] = log_user.id
        return redirect('/success')

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context={
        "posts":MessagePost.objects.all(),
        "all_comments":Comment.objects.all()
    }
    return render(request, "loggedin.html",context)

def post_message(request):
    if request.method == "POST":
        MessagePost.objects.create(
            message = request.POST['message'],
            user_id = User.objects.get(id=request.session['id'])
        )
        return redirect('/success')
    return redirect('/')
    
def post_comment(request, id):
    if request.method == "POST":
        Comment.objects.create(
            comment = request.POST['comment'],
            user_id = User.objects.get(id=request.session['id']),
            message_id = MessagePost.objects.get(id=id)
        )
        return redirect('/success')
    return redirect('/')

def like_post(request, id):
    user_liking = User.objects.get(id=request.session['id'])
    message_liked = MessagePost.objects.get(id=id)
    message_liked.likes.add(user_liking)
    return redirect('/success')

def delete_comment(request,id):
    delete = Comment.objects.get(id=id)
    delete.delete()
    return redirect('/success')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')

def logout(request):
    request.session.flush()
    print("session flushed")
    return redirect('/')
