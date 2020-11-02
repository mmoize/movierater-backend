from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)

# Movie Image Cover Saving logic, save the movies images in a folder named movies in static/media
def get_image_path(instance, filename):
    return os.path.join('movies', str(instance.user), filename)



# Movie Model creates a movie item, with three fields: title, description, image cover
class Movie(TimeStampedModel):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=360)
    image = models.ImageField(upload_to= get_image_path, blank=True)

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

# Rating Model keeps record of the user's actions.
class Rating(TimeStampedModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
     
    # 
    class Meta:
        unique_together = (('user', 'movie'),)
        index_together =  (('user', 'movie'),)
