from django.shortcuts import render, redirect
from django.contrib.auth.hashers import *
# Create your views here.
from django.http import HttpResponse
from frisbee.forms import LoginForm, RegisterForm
from frisbee.models import User, Event, Game, Team

def index(request):
    return render(request,'home.html')

def login(request):
  username = "not logged in"
  if request.method == "POST":
    #Get the posted form
    MyLoginForm = LoginForm(request.POST)
    if MyLoginForm.is_valid():
      username = MyLoginForm.cleaned_data['username']
      return render(request,'test.html',{"test":username})
    else:
      return render(request,'loginerror.html')
  else:
    MyLoginForm = LoginForm()
  return render(request,'login.html')
  
def register(request):
  if request.method == "POST":
    #Get the posted form
    MyRegisterForm = RegisterForm(request.POST)
    if MyRegisterForm.is_valid():
      psw = MyRegisterForm.cleaned_data['psw']
      passwordRepeat = MyRegisterForm.cleaned_data['pswrepeat']
      if(psw != passwordRepeat):
        return render(request,'register_error.html')
      form_email = MyRegisterForm.cleaned_data['email']
      firstname = MyRegisterForm.cleaned_data['firstName']
      lastname = MyRegisterForm.cleaned_data['lastName']
      psw = make_password(psw)
      newUser = User(password = psw, email = form_email, first_name = firstname, last_name = lastname,
       is_leader = False, receive_reminder = False
       )
      newUser.save()
      return render(request,"test.html",{"test": newUser.email})
    else:
      return render(request,'loginerror.html')
  else:
    return render(request,'register.html')