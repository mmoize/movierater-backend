from django.db import models

import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from django_resized import ResizedImageField


def get_image_path(instance, filename):
    return os.path.join('sleekerPostImages', str(instance.user), filename)




class Sleeker(TimeStampedModel):
    description = models.TextField(max_length=360)
    user = models.ForeignKey(User, default=1,  on_delete=models.CASCADE)
    image = models.TextField(max_length=2000) #imageField given a default incase, an image is not provided


    class Meta:
        ordering = ['-created',]


    def __str__(self):
        return self.user.username
