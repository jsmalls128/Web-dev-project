from django import forms
from frisbee.models import User

class LoginForm(forms.Form):
   username = forms.EmailField(max_length = 30)
   password = forms.CharField(widget = forms.PasswordInput())
   
   def clean_message(self):
      username = self.cleaned_data.get("username")
      dbuser = User.objects.filter(email = username)
      if not dbuser:
         raise forms.ValidationError("User does not exist in our db!")
      return username
   
class RegisterForm(forms.Form):
   firstName = forms.CharField(max_length = 20)
   lastName = forms.CharField(max_length = 20)
   email = forms.EmailField(max_length = 30)
   psw = forms.CharField(widget = forms.PasswordInput())
   pswrepeat = forms.CharField(widget = forms.PasswordInput())

class ProfileForm(forms.Form):
   firstName = forms.CharField(max_length = 20)
   lastName = forms.CharField(max_length = 20)
   email = forms.EmailField(max_length = 30)
   psw = forms.CharField(widget = forms.PasswordInput())
   pswrepeat = forms.CharField(widget = forms.PasswordInput())

class TeamForm(forms.Form):
   name = forms.CharField(max_length = 30)

class EventForm(forms.Form):
   name = forms.CharField(max_length = 100)
   location = forms.CharField(max_length = 100)
   date = forms.DateField()
   team_0 = forms.NullBooleanField()
   team_1 = forms.NullBooleanField()
   team_2 = forms.NullBooleanField()
   team_3 = forms.NullBooleanField()
   team_4 = forms.NullBooleanField()
   team_5 = forms.NullBooleanField()
   team_6 = forms.NullBooleanField()
   team_7 = forms.NullBooleanField()
