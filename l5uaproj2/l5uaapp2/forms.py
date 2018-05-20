from django.contrib.auth.models import User
from l5uaapp2.models import UserProfileInfo
from django import forms

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model=User
		fields = ('username','email','password')
		
class UserProfileInfoForm(forms.ModelForm):
	class Meta():
		model=UserProfileInfo
		fields=('portfolio_site','profile_pic')