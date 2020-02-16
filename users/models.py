from django.db import models
from django.contrib.auth.models import AbstractUser


class SnetUser(AbstractUser):

	dob = models.DateField()
	signup_date = models.DateTimeField(auto_now_add=True)
