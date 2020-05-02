from users.models import SnetUser, Profile, Friends, UserCover
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget


class SignUpForm(UserCreationForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput({'placeholder':''})) 
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput({'placeholder':''}))
	class Meta:
		model = SnetUser
		fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
	dob = forms.DateField(label='DOB', input_formats=['%d/%m/%Y'], required=False, widget=forms.TextInput(attrs={
		'id':'datepicker', 'class':'form-control', 'placeholder':'19/9/2000',
		}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
	class Meta:
		model = Profile
		fields = ['image', 'dob']


class UserUpdateForm(forms.ModelForm):
	# Leaving optional to the-- users in updating the fields first_name and last_name
	first_name = forms.CharField(required=False, widget=forms.TextInput(attrs=({'class':'form-control'})))
	last_name = forms.CharField(required=False, widget=forms.TextInput(attrs=({'class':'form-control'})))
	email = forms.EmailField(widget=forms.TextInput(attrs=({'class':'form-control'})))

	class Meta:
		model = SnetUser
		fields = ['email', 'first_name', 'last_name']



class ProfileReadOnlyForm(forms.ModelForm):
	dob = forms.DateField(disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = Profile
		fields = ['dob']


class UserReadOnlyForm(forms.ModelForm):
	first_name = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = SnetUser
		fields = ['first_name', 'last_name', 'email']



class FriendsReqForm(forms.ModelForm):

	class Meta:
		model = Friends
		fields = ['freq']

class FriendsAccpForm(forms.ModelForm):

	class Meta:
		model = Friends
		fields = ['friends']


class CoverPhotoForm(forms.ModelForm):
	cover_photo = forms.ImageField(widget=forms.FileInput(attrs=({'id':'cover_id'})))

	class Meta:
		model = UserCover
		fields = ['cover_photo']