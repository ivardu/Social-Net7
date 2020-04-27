from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from users.managers import CustomUserManager
from PIL import Image


class SnetUser(AbstractUser):
	username = None
	# dob = models.DateField()
	email = models.EmailField(_('email address'), unique=True)
	signup_date = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] 

	objects = CustomUserManager()

	def __str__(self):
		return self.truncate()

	def get_absolute_url(self):
		return reverse('login')

	def truncate(self):
		return f'{self.email}'.split('@')[0]

	def fname_empty(self):
		if self.first_name == '':
			return True
		else:
			return False

	def friend_request(self):
		return Friends.objects.filter(freq_accp_id=self.id).filter(friends='No')

	def friends(self):
		return Friends.objects.filter(Q(freq_accp_id=self.id)|Q(freq_usr_id=self.id)).filter(friends='Yes')

	def frn_list_ids(self):
		self.frn_list_ids = set()
		for frn_obj in self.friends():
			self.frn_list_ids.add(frn_obj.freq_usr.id)
			self.frn_list_ids.add(frn_obj.freq_accp.id)

		return self.frn_list_ids



def profile_img_directory(instance, filename):

	return f'profile_pics/{instance.user.truncate()}/{filename}'


class Profile(models.Model):

	image = models.ImageField(default='default_avatar_profile.jpg', upload_to=profile_img_directory)
	user = models.OneToOneField(SnetUser, on_delete=models.CASCADE)
	dob = models.DateField(null=True, blank=True)

	def __str__(self):
		return f'{self.user.email} Profile'

	def save(self, *args, **kwargs):
		super().save()
		img = Image.open(self.image.path)
		if img.width != 50 or img.height != 50:
			resize = (50,50)
			image = img.resize(resize, Image.ANTIALIAS)
			image.save(self.image.path)

	# def save(self, *args, **kwargs):
	# 	super().save()

	# 	img = Image.open(self.image.path)

	# 	if img.height < 400 or img.width < 400:
	# 		resize = (400, 400)
	# 		image = img.resize(resize, Image.ANTIALIAS)
	# 		image.save(self.image.path)


class Friends(models.Model):
	freq = models.CharField(max_length=3, default='No')
	freq_usr = models.ForeignKey(SnetUser, on_delete=models.CASCADE)
	friends = models.CharField(max_length=3, default='No')
	freq_accp = models.ForeignKey(SnetUser, on_delete=models.CASCADE, related_name='friend_accep')


	def __str__(self):
		return f'{self.freq_usr} {self.freq_accp}' 



def cover_photo_directory(instance, filename):
	return f'{instance.user.email}/cover_photo/{filename}'

class UserCover(models.Model):
	cover_photo = models.ImageField(upload_to=cover_photo_directory)
	user = models.OneToOneField(SnetUser, on_delete=models.CASCADE)


	def save(self, *args, **kwargs):
		super().save()
		img = Image.open(self.cover_photo.path)

		if (img.height < 462 or img.height > 462) and (img.width > 820 or img.width < 820):
			standard_size = (820, 462)
			image = img.resize(standard_size,Image.ANTIALIAS)
			image.save(self.cover_photo.path)