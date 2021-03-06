from django.db.models.signals import post_save
from django.dispatch import receiver 
from users.models import SnetUser, Profile, UserCover

@receiver(post_save, sender=SnetUser)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		UserCover.objects.create(user=instance)

@receiver(post_save, sender=SnetUser)
def update_profile(sender, instance, **kwargs):
	instance.profile.save
