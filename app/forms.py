from django import forms
from app.models import *

class Userform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={'password':forms.PasswordInput}

class Profileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['address','profile_pic']