from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
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


def profile_img_directory(instance, filename):

	return f'profile_pics/{instance.user.email}/{filename}'


class Profile(models.Model):

	image = models.ImageField(default='female.jpg', upload_to=profile_img_directory)
	user = models.OneToOneField(SnetUser, on_delete=models.CASCADE)
	dob = models.DateField(null=True, blank=True)

	def __str__(self):
		return f'{self.user.email} Profile'


class Friends(models.Model):
	freq = models.CharField(max_length=3, default='No')
	freq_usr = models.ForeignKey(SnetUser, on_delete=models.CASCADE)
	friends = models.CharField(max_length=3, default='No')
	freq_accp = models.ForeignKey(SnetUser, on_delete=models.CASCADE, related_name='friend_accep')


	def __str__(self):
		return f'{self.freq_usr} {self.freq_accp}' 




