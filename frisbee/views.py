from django.shortcuts import render, redirect
from django.contrib.auth.hashers import *
# Create your views here.
from django.http import HttpResponse
from frisbee.forms import LoginForm, RegisterForm
from frisbee.models import User, Event, Game, Team

def index(request):
  username = ""
  logStatus = "Login"
  if request.session.has_key('username'):
    username = request.session['username']
    logStatus = "Logout"
  return render(request,'home.html',{"email":username,"login":logStatus})

def login(request):
  if request.method == "POST":
    #Get the posted form
    MyLoginForm = LoginForm(request.POST)
    if MyLoginForm.is_valid():
      username = MyLoginForm.cleaned_data['username']
      password = MyLoginForm.cleaned_data['password']
      if(0 < len(User.objects.filter(email = username))):
        currentAccount = User.objects.get(email = username)
        if(check_password(password,currentAccount.password)):
          request.session['username'] = username
          return redirect(index)
      return render(request,'test.html',{"test":username})
    else:
      return render(request,'loginerror.html')
  else:
    MyLoginForm = LoginForm()
  return render(request,'login.html')

def logout(request):
   try:
      del request.session['username']
   except:
      pass
   return redirect(index)

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