from django import forms

class LoginForm(forms.Form):
   username = forms.CharField(max_length = 30)
   password = forms.CharField(widget = forms.PasswordInput())
   
class RegisterForm(forms.Form):
  firstName = forms.CharField(max_length = 20)
  lastName = forms.CharField(max_length = 20)
  email = forms.EmailField(max_length = 30)
  psw = forms.CharField(widget = forms.PasswordInput())
  pswrepeat = forms.CharField(widget = forms.PasswordInput())