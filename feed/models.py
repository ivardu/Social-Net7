from django.db import models
from users.models import SnetUser

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