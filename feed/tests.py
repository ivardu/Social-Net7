from django.test import TestCase
from feed.models import Feed
from feed import models
from users.models import SnetUser
from django.urls import reverse

# Model Baker external library for testing
from model_bakery import baker

 
class FeedModelTest(TestCase):
	#Feed Model Test Cases

	def setUp(self):
		# Initializing the Feed model with Model Baker 
		self.feed = baker.make('Feed') 

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








