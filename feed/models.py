from django.db import models
from django.urls import reverse
from users.models import SnetUser

from PIL import Image
from datetime import datetime
import pytz

# Method for creating the filesystem path for storaging images of users posts 
def feed_data_directory(instance, filename):
	date = instance.date.date().strftime('%d-%m-%Y')
	return f'feed_data/{instance.user.email}/{date}/{filename}'

# Feed model to store the Users Post info, images(object path), posted_date and user info
class Feed(models.Model):
	post_info = models.CharField(max_length=255, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to=feed_data_directory, blank=True, null=True)
	video = models.FileField(upload_to=feed_data_directory, blank=True, null=True)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)  

	class Meta:
		# resulting the queryset in descending order by date
		ordering = ['-date']


	def save(self, *args, **kwargs):
		super().save()
		# print(self.image)

		if self.image:
			# print("Why I'm true")
			img = Image.open(self.image.path)
			if img.height < 400 or img.width < 400:
				resize = (400, 400)
				image = img.resize(resize, Image.ANTIALIAS)
				image.save(self.image.path)

	def likes_count(self):
		return self.likes_set.count()

	def get_absolute_url(self):
		return reverse('feed:feed')

	def __str__(self):
		return self.user.truncate()+'post'

	def feed_post_time(self):

		self.date_total_seconds = round((datetime.now(tz=pytz.UTC)- self.date).total_seconds())
		self.date_second = self.date_total_seconds
		self.date_minute = self.date_total_seconds//(60)
		self.date_hour = self.date_total_seconds//(60*60)
		self.date_day = self.date_hour//(24)
		self.date_month = self.date_day//30
		self.date_year = self.date_month//12

		if  self.date_year > 0:
			if self.date_year == 1:
				return f'{self.date_year} year ago'	
			return f'{self.date_year} years ago'

		elif self.date_month > 0 and self.date_year < 1:
			if self.date_month == 1:
				return f'{self.date_month} month ago'
			return f'{self.date_month} months ago'

		elif self.date_day > 0 and self.date_month < 1:
			if self.date_day == 1:
				return f'{self.date_day} day ago'
			return f'{self.date_day} days ago'

		elif self.date_hour > 0 and self.date_day < 1:
			if self.date_hour == 1:
				return f'{self.date_hour} hour ago'
			return f'{self.date_hour} hours ago'

		elif self.date_minute > 0 and self.date_hour < 1:
			if self.date_minute == 1:
				return f'{self.date_minute} minute ago'	
			return f'{self.date_minute} minutes ago'

		elif self.date_second > 0 and self.date_minute < 1:
			if self.date_second == 1:
				return f'{self.date_second} second ago'	
			return f'{self.date_second} seconds ago'

		else:
			return f'few moments ago'


	# def 






class Likes(models.Model):
	likes = models.IntegerField()
	feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user} likes'


class Comments(models.Model):

	comments = models.CharField(max_length=255)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)
	feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)



	def __str__(self):
		return f"{self.user} comments"


	class Meta:
		ordering = ['-date']


class CommentLikes(models.Model):
	likes = models.IntegerField()
	like_parent = models.ForeignKey(Comments, on_delete=models.CASCADE)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)


class RelatedComments(models.Model):
	related_comment = models.CharField(max_length=255)
	parent_comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['date']


class RelatedCommentsLikes(models.Model):
	likes = models.IntegerField()
	rc_like_parent = models.ForeignKey(RelatedComments, on_delete=models.CASCADE)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE) 


