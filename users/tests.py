from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, resolve
from django.contrib import auth
from django.conf import settings
from django.test import Client, tag
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

from users.models import SnetUser, Profile, profile_img_directory, Friends
from users.views import SignUpView
from users.forms import( SignUpForm, ProfileUpdateForm, UserUpdateForm, 
	ProfileReadOnlyForm, UserReadOnlyForm, FriendsReqForm, 
	FriendsAccpForm, CoverPhotoForm)
from model_bakery import baker
from unittest.mock import patch
from users.signals import create_profile

from feed.models import Feed

import os, json

User = get_user_model()


def login_func(data={}):
	c = Client()
	signup_url = reverse('register')
	signup_response = c.post(signup_url, data, follow=True)
	# print(Profile.objects.all())

	return (signup_url,signup_response)


class UsersManagersTest(TestCase):
	# User Managers Test Cases

	def test_create_user(self):
		user = User.objects.create_user(email='test@gmail.com', password='foo')
		self.assertEqual(user.email, 'test@gmail.com')
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)

		try:
			# username is none for the AbstractUser option
			# username doesn't exist for the AbstractBaseUser option
			self.assertIsNone(user.username)
		except AttributeError:
			pass
		with self.assertRaises(TypeError):
			User.objects.create_user()
		with self.assertRaises(TypeError):
			User.objects.create_user(email='')
		with self.assertRaises(ValueError):
			User.objects.create_user(email='', password='foo')


	def test_create_superuser(self):

		User = get_user_model()
		user = User.objects.create_superuser(email='superuser@gmail.com', password='foo')

		self.assertEqual(user.email, 'superuser@gmail.com')
		self.assertTrue(user.is_active)
		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)

		try:
			# username is none for the AbstractUser option
			# username doesn't exist for the AbstractBaseUser option
			self.assertIsNone(user.username)

		except AttributeError:
			pass
		with self.assertRaises(ValueError):
			User.objects.create_superuser(email='super@user.com', password='foo', is_superuser=False)

@tag('usermodel')
class UsersModelTest(TestCase):
	# User Model Test Cases
	def setUp(self):
		# Instantiating the model 
		self.snetuser = baker.make(User)

	def test_snetuser(self):
		# Testing the SnetUser model instance and field values
		self.assertIsInstance(self.snetuser, User)
		self.assertIsNone(self.snetuser.username)
		self.assertTrue(self.snetuser.email)
		self.assertTrue(self.snetuser.password)
		self.assertTrue(self.snetuser.__str__(), '<SnetUser: {}'.format(self.snetuser.email))

	def test_snetuser_model_email_truncate_method(self):
		# print(self.snetuser.truncate())
		self.assertTrue(self.snetuser.truncate())
		self.assertTrue(self.snetuser.fname_empty())


class UsersViewsTest(TestCase):
	# Users View Tests	

	def setUp(self):

		self.user_signup_data = {
			'email':'ravi@gmail.com',
			'password1':'Testing@123',
			'password2':'Testing@123',
		}

		self.signup_url,self.signup_response = login_func(self.user_signup_data)
		self.user_signup_data.update(email='ramu@gmail.com')
		self.signup_get_resp = self.client.get(reverse('register'))
		self.login_get_resp = self.client.get(reverse('login'))

		# print(self.login_response)

	def test_signup_and_login_view(self):
		# Testing the template used

		self.assertTemplateUsed(self.signup_get_resp, 'users/signup.html')
		self.assertTemplateUsed(self.login_get_resp,'users/login.html')
		# user = auth.get_user(self.client)
		# self.assertTrue(user.is_authenticated)



	# def test_signup_and_login_csrf(self):
	# 	# CSRF Test
	# 	self.assertContains(self.signup_get_resp, 'csrfmiddlewaretoken')
	# 	self.assertContains(self.login_get_resp,'csrfmiddlewaretoken')

	def test_signup_contains_form(self):
		# Testing the Response of the view to check it contains form or not.
		signup_resp = self.client.get(reverse('register'))
		form = signup_resp.context.get('form')
		self.assertIsInstance(form, SignUpForm)

	def test_signup_with_valid_data(self):
		# Testing SingUp Form data in view with Valid Data
		form = SignUpForm(data=self.user_signup_data)
		form.save()
		self.assertEqual(self.user_signup_data['email'], SnetUser.objects.get(email=self.user_signup_data['email']).email)

	def test_login_with_valid_data(self):	
		SnetUser.objects.create_user(email=self.user_signup_data['email'], password=self.user_signup_data['password1'])
		login_resp  = self.client.post(reverse('login'), {'username':self.user_signup_data['email'],'password':self.user_signup_data['password1']})
		self.assertRedirects(login_resp, reverse('feed:feed'), status_code=302)
		user = auth.get_user(self.client)
		self.assertTrue(user.is_authenticated)

	def test_signup_form_errors(self):
		# If form has errors, posting Invalid data
		response = self.client.post(self.signup_url, {})
		form = response.context.get('form') 
		self.assertTrue(form.errors)

	def test_signup_existing_user(self):
		first_try = self.client.post(reverse('register'), self.user_signup_data)
		second_try = self.client.post(reverse('register'), self.user_signup_data)
		# Will result in 'User with this Email address already exists'.
		self.assertTrue(second_try.context.get('form').errors)

	def test_signup_form_inputs(self):
		self.assertContains(self.signup_get_resp, '<input', 5)
		self.assertContains(self.signup_get_resp, 'type="email"', 1)
		self.assertContains(self.signup_get_resp, 'type="password"', 2)

	# Valid Form Data 

@tag('users_urls')
class UsersURLSTest(TestCase):
	# Users URL's Tests
	
	def test_users_urls(self):
		# SignUp URL Test
		register_url = reverse('register')
		self.assertEqual(register_url, '/')

		# SignUP URL Response code test
		reg_response = self.client.get('/')
		self.assertEqual(reg_response.status_code, 200)

		# SingUp URL View mapping test
		# Testing the URL to see it's resolving to right View mapping test for CBV
		resolver = resolve('/')
		self.assertEqual(resolver.func.__name__, SignUpView.as_view().__name__)

		# Login URL test
		login_url = reverse('login')
		self.assertEqual(login_url,'/login/')

		# Login URL Response code
		log_response = self.client.get('/login/')
		self.assertEqual(log_response.status_code, 200)
		self.assertTemplateUsed(log_response, 'users/login.html')

		# LoginView Mapping to the URL Test
		# Testing the URL to see it's resolving to right View mapping test for CBV
		login_resolve = resolve('/login/')
		self.assertEqual(login_resolve.func.__name__, LoginView.as_view().__name__)

		# logout url View Map Test
		logout_resolve = resolve('/logout/')
		self.assertTrue(logout_resolve.func.__name__,LogoutView.as_view().__name__)

		# Logout View test (Status code, templateUsed, content test )
		logout_resp = self.client.get(reverse('logout'))
		self.assertTemplateUsed(logout_resp, 'users/logout.html')
		self.assertEqual(logout_resp.status_code, 200)
		self.assertContains(logout_resp, 'You have been loggedout')


class UsersFormsTest(TestCase):

	def setUp(self):
		self.data = {
			'email':'123@gmail.com',
			'password1':'Testing@123',
			'password2':'Testing@123',
			'first_name':'Ravi',
			'last_name':'Kumar'
		}

	def test_signup_form_has_fields(self):
		form = SignUpForm()
		expected = ['email','password1','password2']
		actual = list(form.fields)
		self.assertSequenceEqual(expected,actual)

	def test_signup_form_isvalid(self):
		form = SignUpForm(data=self.data)
		self.assertTrue(form.is_valid())
		form_obj = form.save()
		# print(form_obj)
		self.assertTrue(Profile.objects.get(user=form_obj))

	def test_signup_form_is_invalid(self):
		form=SignUpForm(data={})
		self.assertFalse(form.is_valid())

	def test_user_update_form(self):
		form = UserUpdateForm()
		self.assertTrue(form)

	def test_user_update_with_valid_data(self):
		form = UserUpdateForm(data=self.data)
		self.assertTrue(form.is_valid())
		form_obj = form.save()
		self.assertEqual(form_obj.first_name, SnetUser.objects.get(last_name='Kumar').first_name)

	def test_user_update_with_invalid_data(self):
		self.data.update(first_name='', last_name='')
		form = UserUpdateForm(data=self.data)
		# Still the below form passes as the first_name and last_name fields are optional
		self.assertTrue(form.is_valid())


@tag('profile')
class UserProfileTest(TestCase):

	def setUp(self):
		self.user = baker.make(SnetUser)
		self.email = self.user.email,
		self.password = self.user.password
		data = {
			'email':'Ramesh@gmail.com',
			'password1':'Testing@123',
			'password2':'Testing@123',
		}
		self.signup_url,self.signup_response = login_func(data)
		self.client.login(username=data['email'], password=data['password1'])
		self.client.enforce_csrf_checks=True		
		self.profile_resp = self.client.get(reverse('profile'))

		self.resolver = resolve('/profile/') 
		self.new_user = SnetUser.objects.get(email='Ramesh@gmail.com')
		self.ronly_profile = self.client.get(reverse('rprofile', args=(self.user.id,)))
		

	# Testing the Profile Form test

	def test_profile_form_valid(self):
		data = {
			'image':self.user.profile.image,
			'user':self.user.id
		}
		# if instance is not supplied will throw "Profile with user already exists" error so it will fail
		# print(self.user)
		form = ProfileUpdateForm(data=data, instance=self.user.profile)
		# print(form)
		self.assertTrue(form.is_valid())
		form_obj = form.save()
		self.assertIsInstance(form_obj, Profile)

	def test_profile_form_invalid(self):
		form = ProfileUpdateForm(data={})
		# Form gets valid as we are passing empty dict nothing bound form << -- Need to check on this
		self.assertFalse(form.is_valid())
		# But saving data to the model will throw and Integrity error as existing data should need to have user details too.
		with self.assertRaises(IntegrityError):
			form.is_valid()
			form.save()
		
		
	# Actually, django doesn't enforce (by default) csrf checking with tests
	
	# def test_profile_csrf_token(self):
	# 	# self.assertTrue('csrfmiddlewaretoken' in self.profile_resp)
	# 	# print('csrfmiddlewaretoken' in self.profile_resp.content)
	# 	self.assertContains(self.profile_resp, 'csrfmiddlewaretoken')

	# Profile URL, View Mapping and Correct Template rendering test 

	def test_profile_url(self):
		self.assertEqual(self.profile_resp.status_code, 200)

	def test_profile_url_match_view(self):
		self.assertEqual(self.resolver.view_name, 'profile')

	def test_profile_template_used(self):
		# print(self.login_response)
		self.assertTemplateUsed(self.profile_resp, 'users/profile.html')


	###### Testing Signal indirectly as if Profile works ######

	def test_profile_model_instance(self):
		self.assertIsInstance(self.user.profile, Profile)

	def test_profile_model_method(self):
		# print(profile_img_directory(self.profile,self.profile.image))
		self.assertTrue(profile_img_directory(self.user.profile, self.user.profile.image))

	def test_profile_data_saved_or_not(self):
		self.assertEqual(self.user.profile.image, 'default_avatar_profile.jpg')


	def test_profile_resp_data(self):
		# print(self.profile_resp.context.get())
		self.assertContains(self.profile_resp, 'first_name')
		self.assertContains(self.profile_resp, 'last_name')

	# Testing the UserUpdateForm as ProfileUpdateForm both are embeded in same page

	def test_user_update_form(self):
		data = {
			'email':self.user.email,
			'first_name':'Ravi',
			'last_name'	:'Kumar'
		}

		form = UserUpdateForm(data=data, instance=self.user)
		# print(form.errors)
		self.assertTrue(form.is_valid())
		form.save()
		self.assertTrue(SnetUser.objects.get(id=self.user.id).first_name=='Ravi')

	@tag('rprofile')
	def test_rprofile_url(self):
		self.assertEqual(self.ronly_profile.status_code, 200)


@tag('ronly')
class ProfileUsersReadFormTest(TestCase):

	def setUp(self):
		self.user = baker.make(SnetUser)
		self.p_form = ProfileReadOnlyForm(instance=self.user.profile)
		self.u_form = UserReadOnlyForm(instance=self.user)
		self.obj = SnetUser.objects.create(email='ravi@gmail.com')
		self.obj.set_password('Testing@007')
		self.obj.save()
		response = self.client.login(username='ravi@gmail.com', password='Testing@007')
		# self.resp = self.client.get(reverse('rprofile', args=(self.user.id,)))

	def test_profile_read_form(self):
		self.assertTrue(self.p_form)
		self.assertTrue(self.u_form)
		# self.assertContains(self.resp, self.user.email)


@tag('friends')
class FriendsModelTest(ProfileUsersReadFormTest):

	def setUp(self):
		super().setUp()
		self.freq_form = FriendsReqForm()
		self.facp_form = FriendsAccpForm()
		self.req_user = baker.make(SnetUser)
		self.accp_user = SnetUser.objects.create(email='naresh@gmail.com')
		self.accp_user.set_password('Testing@007')
		self.accp_user.save()
		self.client.login(username='ravi@gmail.com', password='Testing@007')
		self.friend_req = self.client.post(reverse('friends_req', args=(self.accp_user.id,)), data={'freq':'Yes'}, follow=True)
		self.rprof_resp = self.client.get(reverse('rprofile', args=(self.req_user.id,)))
		self.client.login(username='naresh@gmail.com', password='Testing@007')
		self.friend_accp = self.client.post(reverse('friends_accp', args=(self.obj.id,)), data={'friends':'Yes'},follow=True)
		# print(self.rprof_resp.context.get('freq_form'))

	def test_friends_model(self):
		self.assertTrue(self.freq_form)
		self.assertTrue(self.facp_form)
		self.assertIn('freq',self.freq_form.fields)
		self.assertIn('friends', self.facp_form.fields)

	def test_url_friends(self):
		self.assertEqual(self.friend_req.status_code, 200)
		self.assertContains(self.friend_req, self.accp_user)
		self.assertContains(self.rprof_resp, 'freq')
		self.assertEqual(self.friend_accp.status_code, 200)

	def test_get_post_urls(self):
		resp_freq = self.client.get(reverse('friends_accp', args=(self.user.id,)))
		self.assertEqual(resp_freq.status_code, 405)
		resp_faccp = self.client.get(reverse('friends_req', args=(self.user.id,)))
		self.assertEqual(resp_faccp.status_code, 405)

@tag('search')
class SearchTest(ProfileUsersReadFormTest):

	def setUp(self):
		super().setUp()
		self.new_user = baker.make(SnetUser)
		self.new_user.first_name = self.new_user.truncate()
		self.new_user.save()
		data = {'search':self.new_user.truncate()}
		self.search_resp = self.client.post(reverse('search'), data=data)
		self.feed = self.client.get(reverse('feed:feed'))
		# print(self.search_resp.content)
		
		# Testing the domain page/home page url redirect post authentication
		self.home_page = self.client.get(reverse('register'), follow=True)

	def test_search_url(self):
		dit = json.loads(self.search_resp.content)[0]
		# print(json.loads(self.search_resp.content))
		self.assertEqual(self.search_resp.status_code, 200)
		self.assertEqual(dit['user'], self.new_user.truncate().capitalize())
		self.assertContains(self.home_page, 'LogOut')
		self.assertEqual(self.home_page.status_code, 200)
		# print(self.search_resp.content)
		self.assertContains(self.search_resp, dit['user'])

	def test_feed_url(self):
		# self.assertContains(self.feed, 'friends')
		# print(self.new_user.friend_request)
		self.assertTrue(self.new_user.friend_request)

@tag('fr_received')
class FriendsTest(ProfileUsersReadFormTest):

	def setUp(self):
		super().setUp()
		file = open(os.path.join(settings.BASE_DIR, 'logged_out.jpg'), 'rb')
		image = SimpleUploadedFile(name=file.name, content=file.read(), content_type='image/jpeg')
		self.new_user = baker.make(SnetUser)
		self.other_user = baker.make(SnetUser)
		self.feed1 = baker.make(Feed, user=self.new_user, image=image)
		self.frd_req = self.client.post(reverse('friends_req', args=(self.new_user.id,)), data={'freq':'Yes'})
		obj = self.new_user.friend_request()[0]
		obj.friends='Yes'
		obj.save()
		self.frd_url_resp = self.client.post(reverse('friend_req_received'))
		self.feed_home = self.client.get(reverse('feed:feed'))

	def test_frd_url(self):
		self.assertEqual(self.frd_url_resp.status_code, 200)
		# Logged in user friends list
		print(self.obj.frn_list_ids())
		self.assertTrue(self.obj.friends())
		# print(self.obj.friend_request())
		self.assertTrue(self.frd_url_resp.context.get('friends'))


	def test_frnd_read_only(self):
		# print(self.feed1)
		# self.assertContainse()
		self.assertContains(self.feed_home, self.feed1.post_info)


@tag('pchange')
class PasswordChangeViewTest(TestCase):

	def setUp(self):
		self.user = SnetUser.objects.create(email='ravi@gmail.com')
		self.user.set_password('Testing@007')
		self.user.save()
		self.client.login(username='ravi@gmail.com', password='Testing@007')
		self.pget_resp = self.client.get(reverse('pchange'))
		

	def test_pass_change(self):
		self.ppost_resp = self.client.post(reverse('pchange'), {'old_password':'Testing@007', 'new_password1':'Daddy@007', 'new_password2':'Daddy@007'}, follow=True)
		self.pc_login_resp = self.client.login(username='ravi@gmail.com', password='Daddy@007')
		self.assertEqual(self.pget_resp.status_code, 200)
		self.assertContains(self.pget_resp, 'password')
		self.assertEqual(self.ppost_resp.status_code, 200)
		#self.ppost_resp contains the login url response as we have set follow = true
		self.assertContains(self.ppost_resp, 'successfully')
		self.assertTrue(self.pc_login_resp)

	# def test_pass_change_post_login(self):





@tag('pass_reset')
class PasswordRestTest(PasswordChangeViewTest):
	def setUp(self):
		super().setUp()
		self.resp = self.client.get(reverse('pass_reset'))
		self.pass_resp = self.client.post(reverse('pass_reset'), {'email':'ravi@gmail.com'})


	def test_pass_reset(self):
		self.assertEqual(self.resp.status_code, 200)
		self.assertContains(self.resp, 'email')
		self.assertEqual(self.pass_resp.status_code, 200)



@tag('cover_photo')
class CoverPhotoTest(TestCase):

	def setUp(self):
		self.user = SnetUser.objects.create(email='ravi@gmail.com')
		self.user.set_password('Testing@007')
		self.user.save()
		self.resp = self.client.login(username='ravi@gmail.com', password='Testing@007')

	def test_cover_photo(self):
		file = open(os.path.join(settings.BASE_DIR, 'logged_out.jpg'), 'rb')
		image = SimpleUploadedFile(name=file.name, content=file.read(), content_type='image/jpeg')

		self.assertTrue(self.resp)
		form = CoverPhotoForm(data={'cover_photo':image, 'user':self.user})
		self.assertTrue(form.is_valid)

	def test_cover_url_view(self):
		self.url = self.client.post(reverse('cover_pic', args=(self.user.id,)))
		self.assertTrue(self.url.status_code, 200)



		



		

		




		

		

