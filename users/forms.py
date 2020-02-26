from users.models import SnetUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput({'placeholder':''})) 
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput({'placeholder':''}))
	class Meta:
		model = SnetUser
		fields = ['email']


# class LoginForm(forms.ModelForm):
# 	password = forms.CharField(label='Password', widget=forms.PasswordInput({'placeholder':''}))
# 	class Meta:
# 		model = SnetUser
# 		fields = ['email', 'password']