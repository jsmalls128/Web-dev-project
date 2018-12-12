from django.shortcuts import render, redirect
from django.contrib.auth.hashers import *
from django.http import HttpResponse
from frisbee.forms import *
from frisbee.models import *
from django.core.mail import send_mail
import datetime
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
def sendMail(request,recipient,hour):
  
  send_mail(
    'Reminder, '+ hour +' hours til kickoff!',
    'Your game starts in '+ hour +' hours!',
    '', # Leave blank
    ['test@gmail.com'], # List of recipients
    fail_silently=False,
)
  return redirect(index)

def confirm(request,uid,token):
  try:
      uid = force_text(urlsafe_base64_decode(uid))
      user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None
  if user is not None and default_token_generator.check_token(user, token):
      user.is_active = True
      user.save()
      # return redirect('home')
      return render(request,'home.html',{"email":"Activation Success!","login":"Login"})
  else:
      return HttpResponse('Activation link is invalid!' + user.first_name)

def sendConf(request,uid,token,email):
  uid = uid.decode("ASCII") 
  send_mail(
    'Registration confirmation',
    'Please go here to confirm your account\n http://172.19.50.140/finalProject/' + uid + '/' + token,
    '', # Leave blank
    [email], # List of recipients
    fail_silently=False,
)
  return render(request,'home.html',{"email":"Please check your email!","login":"Login"})

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
        if(currentAccount.is_active):
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
      #new_user = User.objects.create_user(username=email, email=email, password=psw)
      #new_user.save()
      #token = default_token_generator.make_token(new_user)
      #uid = urlsafe_base64_encode(force_bytes(new_user.pk))
      psw = make_password(psw)
      newUser = User(password = psw, email = form_email, first_name = firstname, last_name = lastname,
       is_leader = False, receive_reminder = False
       )
      newUser.save()
      token = default_token_generator.make_token(newUser)
      uid = urlsafe_base64_encode(force_bytes(newUser.pk))
      return sendConf(request,uid,token,form_email)
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
  if request.session.has_key('username'):
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
      return redirect(profile)
    else:
      return redirect(profile)
  else:
    return redirect(login)

def viewEvent(request, eventid):
  if request.session.has_key('username'):
    username = request.session['username']
    currentAccount = User.objects.get(email = username)
    currentEvent = Event.objects.get(id = eventid)
    eventName = currentEvent.eventName
    date = currentEvent.date
    location = currentEvent.location
    teams = currentEvent.teams.all()
    if currentEvent.user == currentAccount:
      if request.method == 'POST':
        MyEventForm = EventForm(request.POST)
        if MyEventForm.is_valid():
          eventName_form = MyEventForm.cleaned_data['name']
          location_form = MyEventForm.cleaned_data['location']
          date_form = MyEventForm.cleaned_data['date']
          i = 1
          for team in teams:
            form_name = 'team_' + str(i)
            action = request.POST[form_name]
            i = i+1
            if action == "true":
              currentEvent.teams.remove(team)
              currentEvent.save()
          currentEvent.eventName = eventName_form
          currentEvent.location = location_form
          currentEvent.date = date_form
          currentEvent.save()
          teams = currentEvent.teams.all()
          request.method = 'GET'
          return render(request, 'modifyEvent.html', {'date':date_form,'location':location_form,'eventName':eventName_form, 'login':'Logout', 'teams':teams})
        else:
          return render(request, 'modifyEvent.html', {'date':date,'location':location,'eventName':eventName, 'login':'Logout', 'teams':teams})
      elif request.method == 'GET':
        return render(request, 'modifyEvent.html', {'date':date,'location':location,'eventName':eventName, 'login':'Logout', 'teams':teams})
    else:
      return render(request, 'viewEvent.html', {'date':date,'location':location,'eventName':eventName, 'login':'Logout', 'teams':teams, 'is_full':currentEvent.is_full, 'is_leader':currentAccount.is_leader, 'eventid':eventid})
  else:
    redirect(login)

def onGoingEvents(request):
  if request.session.has_key('username'):
    events = Event.objects.all()
    return render(request, 'onGoingEvents.html', {'events':events, 'login':'Logout'})
  else:
    redirect(login)

def joinEvent(request, eventid):
  if request.session.has_key('username'):
    currentAccount = User.objects.get(email = request.session['username'])
    currentAccount.save()
    currentEvent = Event.objects.get(id = eventid)
    currentEvent.save()
    currentEvent.teams.add(currentAccount.team)
    teams = currentEvent.teams.all()
    if teams.count == 8:
      currentEvent.is_full = True
      currentEvent.save()
    else:
      currentEvent.save()
    return redirect(viewEvent, eventid)
  else:
    return redirect(login)

def removeplayer(request):
  if request.session.has_key('username'):
    currentAccount = User.objects.get(email = request.session['username'])
    if(currentAccount.is_leader):
      memberList = request.POST
      currentTeam = currentAccount.team
      itermembers = iter(memberList)
      next(itermembers)
      for member in itermembers:
        removeEmail = memberList[member]
        deleteMember = User.objects.get(email = removeEmail, team = currentTeam)
        deleteMember.team = None
        deleteMember.save()
      return redirect(profile)
  return redirect(login)