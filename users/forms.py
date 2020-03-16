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
	dob = forms.DateField(input_formats=['%d/%m/%Y'], required=False)
	class Meta:
		model = Profile
		fields = '__all__'


class UserUpdateForm(forms.ModelForm):
	# Leaving optional to the users in updating the fields first_name and last_name
	# first_name = forms.CharField()
	# last_name = forms.CharField()

	class Meta:
		model = SnetUser
		fields = ['email', 'first_name', 'last_name']