from django.http import request
from exam_app.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
import datetime
# Create your views here.
def home (request):
# user's home page where they can see all their wishes
    logged_user= User.objects.get(id=request.session['user'])
    context = {
        "all_wishes": Wish.objects.all(),
        "users_info": User.objects.get(id=request.session['user'])
    }
    return render(request, 'exam/index.html', context)

def logout (request):
# log the user out and return them to login and registration page
    request.session.flush()
    return redirect('/')


def new (request):
# shows a page where the user can create a new wish
    context ={
        "users_info": User.objects.get(id=request.session['user'])
    }
    return render(request, 'exam/new.html', context)

def create (request):
# creates a new wish to add to database
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        logged_user = User.objects.get(id=request.session['user'])
        if len(errors) > 0:
            for value in errors.items():
                messages.error(request,value)
            return redirect ('/wishes/new')

        added_wish = Wish.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            uploaded_by = logged_user,
        )
        # added_wish.users_who_like.add(logged_user)
    return redirect('/wishes/home')

def edit (request, wish_id):
# where the user can edit their wish
    wish_to_edit = Wish.objects.get(id=wish_id)
    users_info = User.objects.get(id=request.session['user'])
    context = {
        "users_info": User.objects.get(id=request.session['user']),
        "wish": wish_to_edit,
    }
    return render( request, 'exam/edit.html',context)

def update (request, wish_id):
# method to actually edit the book
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for value in errors.items():
                messages.error(request,value)
            return redirect(f'/wishes/edit/{wish_id}')

        make_update = Wish.objects.get(id=wish_id)
        make_update.title = request.POST['title']
        make_update.description = request.POST['description']
        make_update.save()
    return redirect('/wishes/home')

def delete (request, wish_id):
# deletes a wish from the database if the person created it
    if request.method == "POST":
        wish_to_delete = Wish.objects.get(id=wish_id)
        if wish_to_delete.uploaded_by.id == request.session['user']:
            wish_to_delete.delete()
    return redirect('/wishes/home')

def granted (request, wish_id):
# moves the granted wish from the top table to the bottom table
    if request.method == "POST":
        wish_to_grant = Wish.objects.get(id=wish_id)
        wish_to_grant.granted_at = datetime.datetime.now()
        wish_to_grant.save()
    return redirect('/wishes/home')

def stats(request):
# renders a stats page for the user to see their stats
    all_granted_wishes = Wish.objects.exclude(granted_at = None)
    all_ungranted_wishes = Wish.objects.filter(granted_at = None)
    users_info = User.objects.get(id=request.session['user'])
    my_granted_wishes = all_granted_wishes.filter(uploaded_by=users_info)
    my_pending_wishes = all_ungranted_wishes.filter(uploaded_by=users_info)
    context ={
        "users_info":users_info,
        "all_granted_wishes": all_granted_wishes,
        "my_granted_wishes": my_granted_wishes,
        "my_pending_wishes": my_pending_wishes,
    }
    return render(request, 'exam/stats.html', context)

def like (request, wish_id):
# adds a like to a specific user's wish
    logged_user = User.objects.get(id=request.session['user'])
    wish = Wish.objects.get(id=wish_id)
    wish.users_who_like.add(logged_user)
    return redirect('/wishes/home')
