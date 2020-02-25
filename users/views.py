from django.shortcuts import render
from django.views.generic.edit import CreateView
from users.forms import SignUpForm, LoginForm


class SignUpView(CreateView):
	# User SignUp Class based view
	form_class = SignUpForm
	template_name = 'users/signup.html'


class LoginView(CreateView):

	form_class = LoginForm
	template_name = 'users/login.html'