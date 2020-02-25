from django.db import models
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