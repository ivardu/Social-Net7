from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView
from django.views.decorators.http import require_POST
# from django.contrib.auth.views import UserCreation
from users.forms import SignUpForm, ProfileUpdateForm, UserUpdateForm, ProfileReadOnlyForm, UserReadOnlyForm, FriendsReqForm, FriendsAccpForm
from users.models import SnetUser, Friends
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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


	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('feed:feed'))
		return super().get(self, *args, **kwargs)


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


@login_required
def rprofile(request, id):
	user = SnetUser.objects.get(pk=id)
	p_form = ProfileReadOnlyForm(instance=user.profile)
	u_form = UserReadOnlyForm(instance=user)
	freq_form = FriendsReqForm()

	try:
		freq = Friends.objects.filter(Q(freq_usr=user)|Q(freq_accp=user)).filter(Q(freq_usr=request.user)|Q(freq_accp=request.user)).filter(freq='Yes')
		# print(freq)
		if freq[0].friends == 'No':
			freq_sent = freq[0]
		elif freq[0].friends == 'Yes':
			freq_sent = freq[0]
	except:
		# print('No User')
		pass

	return render(request, 'users/rprofile.html', locals())

@login_required
@require_POST
def friends_req(request, id):
	req_user = request.user
	accp_user = SnetUser.objects.get(pk=id)
		
		# new_frn_req = Friends.objects.filter(freq_accp=req_user).filter(friends='No')

	if request.method == 'POST':
		form = FriendsReqForm(request.POST)
		if form.is_valid():
			freq_obj = form.save(commit=False)
			freq_obj.freq = 'Yes'
			freq_obj.freq_accp = accp_user
			freq_obj.freq_usr = req_user
			freq_obj.save()
			# print(freq_obj.freq_usr, freq_obj.freq_accp)
		return HttpResponseRedirect(reverse('rprofile', args=(accp_user.id,)))


	# return HttpResponse('Fail')
@login_required
@require_POST
def friends_accp(request, id):
	accp_user = request.user 
	req_user = SnetUser.objects.get(pk=id)
	friends = Friends.objects.filter(freq_usr=req_user).filter(freq_accp=accp_user).filter(freq='Yes')
	if request.method == 'POST':
		if friends[0].friends == 'No':
			form = FriendsAccpForm(request.POST, instance=friends[0])
		if form.is_valid():
			obj = form.save(commit=False)
			obj.friends = 'Yes'
			obj.save()

		return HttpResponseRedirect(reverse('rprofile', args=(req_user.id,)))

	# return HttpResponse('Fail')
@login_required
def search(request):
	result = request.POST.get('search')
	no_result = 'No Results Found'
	if result:
		name_list = SnetUser.objects.filter(Q(first_name=result)|Q(last_name=result)|Q(email__contains=result))
		# print(name_list)

	return render(request, 'users/search.html', locals())

@login_required
def friend_req_received(request):
	# print(request.user.friend_request())
	frend_req_list = request.user.friend_request()
	friends = request.user.friends()
	# print(frend_req_list, type(request.user.friend_request()))
	return render(request, 'users/friends.html', locals())
