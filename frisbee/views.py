from django.shortcuts import render, redirect
from django.contrib.auth.hashers import *
from django.http import HttpResponse
from frisbee.forms import *
from frisbee.models import *
from django.core.mail import send_mail

def sendMail(request,recipient,hour):
  
  send_mail(
    'Reminder, '+ hour +' hours til kickoff!',
    'Your game starts in '+ hour +' hours!',
    '', # Leave blank
    ['test@gmail.com'], # List of recipients
    fail_silently=False,
)
  return redirect(index)
  
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
    return render(request,'loginerror.html')
  else:
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
      return redirect(index)
    else:
      return render(request,'loginerror.html')
  else:
    return render(request,'register.html')
    
def profile(request):
  teamroster = []
  team = ""
  teamFunction = "Create"
  events = None
  if request.session.has_key('username'):
    username = request.session['username']
    currentAccount = User.objects.get(email = username)
    try:
      events = Event.objects.filter(user = currentAccount)
    except Event.DoesNotExist:
      events = None
    if request.method == "POST":
    #Get the posted form
      MyProfileForm = ProfileForm(request.POST)
      if MyProfileForm.is_valid():
        psw = MyProfileForm.cleaned_data['psw']
        passwordRepeat = MyProfileForm.cleaned_data['pswrepeat']
        if(psw != passwordRepeat):
          return redirect(index)
        form_email = MyProfileForm.cleaned_data['email']
        firstname = MyProfileForm.cleaned_data['firstName']
        lastname = MyProfileForm.cleaned_data['lastName']
        if(check_password(psw,currentAccount.password)):
          currentAccount.email = form_email
          currentAccount.first_name = firstname
          currentAccount.last_name = lastname
          try:
            del request.session['username']
          except:
            pass
          request.session['username'] = currentAccount.email
          currentAccount.save()
    if currentAccount.team is not None:
      team = currentAccount.team
      if currentAccount.is_leader:
        teamFunction = "Manage"
        teamroster = User.objects.filter(team = team)
    return render(request,'profile.html',{"Account":currentAccount, "last_name": currentAccount,
    "email":currentAccount,"team":team, "manage":teamFunction, "roster":teamroster, "events":events, "login":"Logout"})
  return redirect(login)

def createTeam(request):
  if request.method == "POST":
    myTeamForm = TeamForm(request.POST)
    if myTeamForm.is_valid():
      teamName = myTeamForm.cleaned_data['name']
      newTeam = Team(team_name = teamName, win_count = 0, loss_count = 0, tie_count = 0)
      newTeam.save()
      username = request.session['username']
      currentAccount = User.objects.get(email = username)
      currentAccount.team = newTeam
      currentAccount.is_leader = True
      currentAccount.save()
      return redirect(profile)
  return redirect(index)

def createEvent(request):
  if request.method == "POST":
    MyEventForm = EventForm(request.POST)
    if MyEventForm.is_valid():
      eventName = MyEventForm.cleaned_data['name']
      location = MyEventForm.cleaned_data['location']
      date = MyEventForm.cleaned_data['date']
      username = request.session['username']
      currentAccount = User.objects.get(email = username)
      newEvent = Event(eventName = eventName, location = location, date = date)
      newEvent.user = currentAccount
      newEvent.save()
      return redirect(profile)
  return redirect(index)

def viewEvent(request, eventid):
  if request.session.has_key('username'):
    username = request.session['username']
    currentAccount = User.objects.get(email = username)
    currentEvent = Event.objects.get(id = eventid)
    eventName = currentEvent.eventName
    date = currentEvent.date
    location = currentEvent.date
    if currentEvent.user == currentAccount:
      if request.method == 'POST':
        MyEventForm = EventForm(request.POST)
        eventName_form = MyEventForm.cleaned_data['name']
        location_form = MyEventForm.cleaned_data['location']
        date_form = MyEventForm.cleaned_data['date']
        currentEvent.eventName = eventName_form
        currentEvent.location = location_form
        currentEvent.date = date_form
        currentEvent.save()
        return redirect(viewEvent)
      elif request.method == 'GET':
        return render(request, 'modifyEvent.html', {'date':date,'location':location,'eventName':eventName, 'login':'LogOut'})
    else:
      return render(request, 'viewEvent.html', {'date':date,'location':location,'eventName':eventName, 'login':'LogOut'})
