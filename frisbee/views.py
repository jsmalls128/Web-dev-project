from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from frisbee.forms import LoginForm

def index(request):
    return render(request,'home.html')

def login(request):
  username = "not logged in"
  if request.method == "POST":
    #Get the posted form
    MyLoginForm = LoginForm(request.POST)
    if MyLoginForm.is_valid():
      username = MyLoginForm.cleaned_data['username']
    return redirect(loginerror)
  else:
    MyLoginForm = LoginForm()
  return render(request,'login.html')