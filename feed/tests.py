from django.test import TestCase
from django.urls import reverse
from django.conf import settings 
from django.core.files.uploadedfile import SimpleUploadedFile
from feed.models import Feed
from feed import models
from feed.forms import FeedForm
from users.models import SnetUser
import os
from io import BytesIO

from model_bakery import baker

# Model Baker external library for testing
from model_bakery import baker

file = open(os.path.join(settings.BASE_DIR, 'logged_out.jpg'), 'rb')
image = {'image':SimpleUploadedFile(name=file.name, content=file.read(), content_type='image/jpeg')}

 
class FeedModelTest(TestCase):
	#Feed Model Test Cases

	def setUp(self):
		# Initializing the Feed model with Model Baker 
		self.feed = baker.make('Feed')
		# self.client.login(username='Ramesh@gmail.com', password='') 

	def test_feed(self):
		# Testing the Feed model data 
		self.assertEqual(Feed.objects.count(),1)
		self.assertIsInstance(self.feed.user, SnetUser)

	def test_feed_data_directory(self):
		# Testing the feed model method data directory
		self.assertTrue(models.feed_data_directory(self.feed, self.feed.image))

		with self.assertRaises(TypeError):
			models.feed_data_directory(self.feed.image)

		with self.assertRaises(TypeError):
			models.feed_data_directory()

		with self.assertRaises(AttributeError):
			models.feed_data_directory('', self.feed.image)


class FeedURLSTest(TestCase):

	def setUp(self):
		self.feed_url = reverse('feed:feed')
		self.feed_url_resp = self.client.get(self.feed_url) 
		self.user = SnetUser.objects.create(email='Test@gmail.com')
		self.user.set_password('Testing@007')
		self.user.save()
		self.data ={
			'email':self.user.email,
			'password':'Testing@007'
		} 

	def test_feed_url(self):
		# print(self.feed_url_resp)
		self.assertEqual(self.feed_url_resp.status_code, 302)
		self.assertRedirects(self.feed_url_resp, '/login/?next=/feed/', status_code=302)

	def test_feed_url_login_decorator(self):
		self.client.login(email=self.data['email'], password=self.data['password'])
		resp = self.client.get(reverse('feed:feed'))
		self.assertEqual(resp.status_code, 200)


class FeedViewTest(TestCase):

	def setUp(self):
		file = open(os.path.join(settings.BASE_DIR, 'logged_out.jpg'),'rb')
		image = SimpleUploadedFile(name=file.name, content=file.read(), content_type='image/jpeg')
		self.feed_url = reverse('feed:feed')
		self.user = SnetUser.objects.create(email='Test@gmail.com', password='Testing@007')
		self.user.set_password('Testing@007')
		self.user.save()
		self.data = {
			'email':self.user.email,
			'password':'Testing@007'
		} 
		self.feed_data = {
			'post_info': 'Testing',
			'image': image,
			'user': self.user.id,
		}

	def test_feed_post_save(self):
		self.client.login(email=self.data['email'], password=self.data['password'])
		self.client.post(self.feed_url, data=self.feed_data)
		# Testing Feed data saved or not
		self.assertTrue(Feed.objects.filter(post_info='Testing'))
		# print(Feed.objects.filter(post_info='Testing'))
		# Testing Feedlist is passed to same template or not - checking first object of query set
		feed_response = self.client.get(reverse('feed:feed'))
		self.assertEqual(feed_response.context.get('feed')[0].user.email,'Test@gmail.com')


class FeedFormTest(TestCase):

	def setUp(self):
		self.user = baker.make(SnetUser)
		# self.user_new = SnetUser.objects.create(email='ravi_new@gmail.com')
		# self.user_new.set_password('Testing@007')
		# self.user_new.save()
		# self.feed_test = baker.make(Feed, _create_files=True)
		self.data = {
			'post_info':'Test_data',
			'user': self.user.id,
		}

	def test_feed_form_has_fields(self):
		form = FeedForm()
		expected = ['post_info','image']
		actual = list(form.fields)
		self.assertSequenceEqual(expected, actual)

	def test_feed_form_is_valid(self):
		form = FeedForm(self.data, image)
		self.assertTrue(form.is_valid())

	def test_feed_form_is_invalid(self):
		form = FeedForm(self.data)
		self.assertFalse(form.is_valid())











