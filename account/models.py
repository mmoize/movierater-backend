from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import random

from django.db import models
from django.contrib.auth.models import User

random_number = random.randint(1, 11)

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.user), filename)


DEFAULT = 'default-'+ str(random_number) + '.png'


# Profile class Creates a profile every time a user signs up
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to= get_image_path, default=DEFAULT) #imageField given a default incase, an image is not provided
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)





    # Profile will be defined by username field.
    def __str__(self):
        return self.user.username

# Signal Logic for triggering profile creation.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.username = instance.username
        profile.save()
post_save.connect(create_user_profile, sender=User, dispatch_uid="users-profilecreation-signal")




