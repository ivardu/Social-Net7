from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView
# from django.contrib.auth.views import UserCreation
from users.forms import SignUpForm, ProfileUpdateForm, UserUpdateForm, ProfileReadOnlyForm, UserReadOnlyForm
from users.models import SnetUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class SignUpView(CreateView):
	# User SignUp Class based view
	form_class = SignUpForm
	model = SnetUser
	# fields = ['email','password']
	template_name = 'users/signup.html'
	# success_url = reverse_lazy('login')

	# def form_valid(self, form):
	# 	form.save()
	# 	return super().form_valid(form)

	# def form_invalid(self, form):
	# 	return super().form_invalid(form)


@login_required
def profile(request):
	if request.method == 'POST':
		# print(request.user.profile)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		user_form = UserUpdateForm(request.POST, instance=request.user)
		if profile_form.is_valid() and user_form.is_valid():
			profile_form.save()	
			user_form.save()
			messages.success(request, f'Successfully updated profile')
			return HttpResponseRedirect(reverse('profile'))
	else:
		profile_form = ProfileUpdateForm(instance=request.user.profile)
		user_form = UserUpdateForm(instance=request.user)


	return render(request, 'users/profile.html', locals())



def rprofile(request, id):
	user = SnetUser.objects.get(pk=id)
	p_form = ProfileReadOnlyForm(instance=user.profile)
	u_form = UserReadOnlyForm(instance=user)

	return render(request, 'users/rprofile.html', locals())
