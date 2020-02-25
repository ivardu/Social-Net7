from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from users.models import SnetUser
from users.views import SignUpView
from model_bakery import baker

User = get_user_model()

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




class UsersViewsTest(TestCase):
	# Users View Tests
	def test_users_url_views(self):
		# Testing the URL to see it's resolving to right View
		resolver = resolve('/')
		self.assertEqual(resolver.func.__name__, SignUpView.as_view().__name__)

		login_resolver = resolve('/login/')
		self.assertEqual(login_resolver.url_name, 'login')




class UsersURLSTest(TestCase):
	# Users URL's Tests
	def test_users_urls(self):
		register_url = reverse('register')
		self.assertEqual(register_url, '/')

		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

		# self.assertTrue('email' in response.context)
		# print(response.context)
		login_url = reverse('login')
		self.assertEqual(login_url, '/login/')
