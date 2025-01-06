from django.shortcuts import render , reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from users.forms import UserForm
from django.contrib.auth.models import User
from main.functions import generate_form_errors
from posts.models import Author


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request,username=username, password=password)
            if user is not None:
                auth_login(request, user)

                return HttpResponseRedirect("/")

        
        context={
            'title': 'Login',
            "error":True,
            "message":"Invalid username or password"

        }
        return render(request, 'users/login.html',context=context)
    else:
        context={
            'title': 'Login'
        }
    return render(request, 'users/login.html',context=context)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("web:index"))

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            instace = form.save(commit=False)
            User.objects.create_user(
                username = instace.username,
                password = instace.password,
                email = instace.email,
                first_name = instace.first_name,
                last_name = instace.last_name,
            )
            Author.objects.create(name = instace.first_name,user = user)
            user = authenticate(request, username = instace.username,password = instace.password)
            auth_login(request,user)

            return HttpResponseRedirect(reverse("web:index"))
        else:
            message = generate_form_errors(form)
            form = UserForm()
            context={
            'title': 'Signup',
            "error":True,
            "message":message,
            "form":form,
            }
            return render(request , "users/signup.html", context=context)
    else:
        form = UserForm()
        context = {
            "title":"Signup",
            "form":form,
        }
        return render(request,"users/signup.html",context=context)