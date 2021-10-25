import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from django_resized import ResizedImageField

# Movie Image Cover Saving logic, save the movies images in a folder named movies in static/media
def get_image_path(instance, filename):
    return os.path.join('movies', str(instance.user), filename)

# Movie Model creates a movie item, with three fields: title, description, image cover
class Movie(TimeStampedModel):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=360)
    user = models.ForeignKey(User, default=1,  on_delete=models.CASCADE)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)
    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

    class Meta:
        ordering = ['-created',]
        
# Rating Model keeps record of the user's actions.
class Rating(TimeStampedModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
     
    # 
    class Meta:
        unique_together = (('user', 'movie'),)
        index_together =  (('user', 'movie'),)
    

def Movie_image_path(instance, filename):
    return os.path.join('MoviesImage', str(instance.movie.user), filename)

class MoviesImage(TimeStampedModel):
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= Movie_image_path)
    user = models.ForeignKey(User, default="1", on_delete=models.CASCADE)



    def __str__(self):
        template = '{0.user.username} {0.movie.title}'
        return template.format(self)

    class Meta:
        ordering = ['-created',]


