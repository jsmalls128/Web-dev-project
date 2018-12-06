from django import forms
from frisbee.models import User

class LoginForm(forms.Form):
   username = forms.CharField(max_length = 30)
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