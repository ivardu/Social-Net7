from django.db import models
from users.models import SnetUser
from PIL import Image

# Method for creating the filesystem path for storaging images of users posts 
def feed_data_directory(instance, filename):
	date = instance.date.date().strftime('%d-%m-%Y')
	return f'feed_data/{instance.user.email}/{date}/{filename}'

# Feed model to store the Users Post info, images(object path), posted_date and user info
class Feed(models.Model):
	post_info = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to=feed_data_directory)
	user = models.ForeignKey(SnetUser, on_delete=models.CASCADE)  

	class Meta:
		ordering = ['-date']


	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.image.path)

		if img.height < 400 or img.width < 400:
			resize = (400, 400)
			image = img.resize(resize, Image.ANTIALIAS)
			image.save(self.image.path)


class Likes(models.Model):
	likes = models.IntegerField()
	feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

