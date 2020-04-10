from django.test import TestCase
from django.urls import reverse
from django.conf import settings 
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.contrib import auth
from django.test import tag
from feed.models import Feed, Likes, Comments
from feed import models
from feed.forms import FeedForm, CommentsForm, LikesForm
from users.models import SnetUser
from users.forms import SignUpForm 
import os
from unittest import mock
from io import BytesIO
import datetime

from model_bakery import baker

# Model Baker external library for testing
from model_bakery import baker

file = open(os.path.join(settings.BASE_DIR, 'logged_out.jpg'), 'rb')
image = {'image':SimpleUploadedFile(name=file.name, content=file.read(), content_type='image/jpeg')}

 
class FeedModelTest(TestCase):
	#Feed Model Test Cases

	def setUp(self):
		# Initializing the Feed model with Model Baker 
		try:
			# image = mock.MagicMock(spec=File)
			# image.name = 'Test_image'
			self.feed = baker.make('Feed', image=image['image'])

		except Exception as e:
			print(e)
		 # image = mock.MagicMock(spec=File, name='Test_image')


		# print(self.feed.image)
		# pass
		# if self.feed.image:
		# 	print(True)
		# else:
		# 	print(False)
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
		self.assertContains(feed_response, 'feed')

@tag('feed_data')
class FeedFormTest(TestCase):

	def setUp(self):
		self.user = baker.make(SnetUser)
		# self.user_new = SnetUser.objects.create(email='ravi_new@gmail.com')
		# self.user_new.set_password('Testing@007')
		# self.user_new.save()
		# self.feed_test = baker.make(Feed, _create_files=True)
		file = open(os.path.join(settings.BASE_DIR, 'logged_out.jpg'), 'rb')
		self.image = {'image':SimpleUploadedFile(name=file.name, content=file.read(), content_type='image/jpeg')}
		self.data = {
			'post_info':'Test_data',
			# 'user': self.user,
		}

	def test_feed_form_has_fields(self):
		form = FeedForm()
		expected = ['post_info','image']
		actual = list(form.fields)
		self.assertSequenceEqual(expected, actual)

	def test_feed_form_is_valid(self):
		# self.data.update(image)
		# print(self.data)
		form = FeedForm(self.data, self.image)
		print(form.errors)
		self.assertTrue(form.is_valid())

	def test_feed_form_is_invalid(self):
		form = FeedForm(self.data)
		self.assertFalse(form.is_valid())

	# def test_feed_form_list(self):

@tag('likes')
class LikeModelTest(TestCase):

	def setUp(self):
		self.feed = baker.make(Feed, image=image['image'])
		self.user = baker.make(SnetUser)
		self.likes = baker.make(Likes, likes=0, feed=self.feed, user=self.user)
		self.likes_url_get = self.client.get(reverse('feed:likes', args=(self.feed.id,)))
		self.data = {
			'email':'ravi@gmail.com', 
			'password1':'Testing@007', 
			'password2':'Testing@007'
		}
		form = SignUpForm(self.data)
		form.save()
		resp = self.client.login(username=self.data['email'], password='Testing@007')
		self.user_new = SnetUser.objects.get(email=self.data['email'])
		self.likes_url_post = self.client.post(reverse('feed:likes', args=(self.feed.id,)), {'likes':(self.likes.likes)+1, 'feed':self.feed, 'user':self.user_new.id})
		self.feed_resp = self.client.get(reverse('feed:feed')) 
		self.dupl_data = {
			'likes':1,
			'feed':self.feed.id,
			'user':self.user_new.id
		}

	def test_likes_model(self):
		self.assertIsInstance(self.likes, Likes)

	def test_likes_attr_count(self):
		# print(self.likes.likes)
		self.assertEqual(self.likes.likes,0)

	def test_likes_url_post(self):
		self.assertEqual(self.likes_url_post.status_code, 302)
		# print(Likes.objects.all())
		# print(Likes.objects.get(user=self.user_new))
		self.assertEqual((Feed.objects.get(pk=self.feed.id)).likes_set.get(user=self.user_new).likes, 1)
		self.assertEqual((Feed.objects.get(pk=self.feed.id)).likes_set.filter(likes=1).count(),1)

	def test_likes_duplicate(self):
		likes_form = LikesForm(data=self.dupl_data)
		self.assertTrue(likes_form.is_valid())
		resp = self.client.post(reverse('feed:likes', args=(self.feed.id,)), {'likes':1, 'feed':self.feed, 'user':self.user_new.id})
		# self.assertContains(resp, 'Failing')
		self.assertEqual(len(Likes.objects.filter(feed=self.feed).filter(user=self.user_new)),1)
		


@tag('comments')
class CommentModelTest(TestCase):

	def setUp(self):
		self.test = {
				'email':'ravi_new@gmail.com',
				'password1':'Daddy@007',
				'password2':'Daddy@007'
		}
		self.obj = SnetUser.objects.create(email=self.test['email'])
		self.obj.set_password(self.test['password1'])
		self.obj.save()
		self.feed = baker.make(Feed, image=image['image'], user=self.obj)
		self.coment = baker.make(Comments, feed=self.feed)
		self.user = baker.make(SnetUser)
		self.comment = Comments.objects.get(pk=1)
		self.data = {
			'comments':'Hello World',
			'user':self.user,
			'feed':self.feed
		}
		resp = self.client.login(username=self.test['email'], password=self.test['password1'])
		self.comm_resp = self.client.post(reverse('feed:comments', args=(self.feed.id,)), {'comments':'Hello World'})


	def test_comment_model(self):
		print('Comment 1')
		self.assertIsInstance(self.comment, Comments)

	def test_commet_form_valid(self):
		print('Comment 2')
		form = CommentsForm(data=self.data)
		self.assertTrue(form.is_valid())

	def test_comment_form_invalid(self):
		print('Comment 3')
		form = CommentsForm(data={})
		self.assertFalse(form.is_valid())

	def test_comment_status_code(self):
		print('Comment 4')
		self.assertEqual(self.comm_resp.status_code, 302)

	def test_comment_model_object(self):
		print('Comment 5')
		comment = Comments.objects.get(comments='Hello World')
		self.assertEqual('Hello World',comment.comments)

@tag('myposts')
class MyPostsViewsTest(CommentModelTest):
	@tag('only_myposts')
	def test_myposts_response(self):
		self.resp = self.client.get(reverse('feed:myposts', args=(self.obj.id,)))
		self.assertEqual(self.resp.status_code, 200)
		self.assertContains(self.resp, self.obj.truncate())
		self.assertContains(self.resp, "logged_out")
		self.assertContains(self.resp, 'comments')

	def test_url_check(self):
		self.resp = self.client.get(reverse('feed:myposts', args=(self.obj.id,)))
		self.assertContains(self.resp, 'Search')


@tag('feed_edit')
class FeedEditTest(CommentModelTest):

	def setUp(self):
		super().setUp()
		self.resp = self.client.post(reverse('feed:feed_edit', args=(self.feed.id,)), {'post_info':'New data'})

	def test_edit_feed_model(self):
		self.feed.refresh_from_db()
		self.assertEqual(self.feed.post_info, 'New data')
		
@tag('feed_del')
class FeedDeleteTest(CommentModelTest):

	def setUp(self):
		super().setUp()

	@tag('fd1')
	def test_feed_exits(self):
		self.ff = self.client.get(reverse('feed:feed'))
		# print(self.feed_feed)
		self.assertTrue(Feed.objects.filter(id=self.feed.id))
		self.assertContains(self.ff, 'Del')
		# user = auth.get_user(self.client)
		# print(user.is_authenticated)

	@tag('fd1')
	def test_feed_delete(self):
		self.feed_delete = self.client.post(reverse('feed:feed_del', args=(self.feed.id,)))
		self.assertEqual(self.feed_delete.status_code, 302)


	












