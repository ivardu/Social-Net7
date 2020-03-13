from users.models import SnetUser, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput({'placeholder':''})) 
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput({'placeholder':''}))
	class Meta:
		model = SnetUser
		fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
	dob = forms.DateField(input_formats=['%d/%m/%Y'])
	class Meta:
		model = Profile
		fields = '__all__'