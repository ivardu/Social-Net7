from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from users.managers import CustomUserManager

class SnetUser(AbstractUser):
	username = None
	# dob = models.DateField()
	email = models.EmailField(_('email address'), unique=True)
	signup_date = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] 

	objects = CustomUserManager()

	def __str__(self):
		return self.email

	def get_absolute_url(self):
		return reverse('login')


def profile_img_directory(instance, filename):

	return f'profile_pics/{instance.user.email}/{filename}'


class Profile(models.Model):

	image = models.ImageField(default='female.jpg', upload_to=profile_img_directory)
	user = models.OneToOneField(SnetUser, on_delete=models.CASCADE)
	dob = models.DateField()

	def __str__(self):
		return f'{self.user.email} Profile'