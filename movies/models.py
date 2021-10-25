import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import DateField
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from django_resized import ResizedImageField



class Movie(TimeStampedModel):
    title = models.CharField(max_length=30)
    plot = models.TextField(max_length=5000)
    poster =models.TextField(max_length=5000)
    director = models.CharField(max_length=30)
    released = models.DateField()
    year =  models.CharField(max_length=30)
    genre = models.CharField(max_length=30)
    imdbid = models.CharField(max_length=30)
    runtime = models.CharField(max_length=30)


    def no_of_ratings(self):
        ratings = Movierating.objects.filter(movie=self)
        return len(ratings)
    def avg_rating(self):
        sum = 0
        ratings = Movierating.objects.filter(movie=self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum / len(ratings)
        else: 
            return 0

    class Meta:
        ordering = ['-created',]


class Movierating(TimeStampedModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
     
    # 
    class Meta:
        unique_together = (('user', 'movie'),)
        index_together =  (('user', 'movie'),)


class Review(TimeStampedModel):
    movie = models.ForeignKey(Movie, related_name="movies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_body = models.TextField()


    def __str__(self):
        return '%s - %s' % (self.movie.title, self.user.username)

    class Meta:
        ordering = ['-created',]



class Comment(TimeStampedModel):
    review = models.ForeignKey(Review, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_body = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.review.movie.title, self.user.username)

    class Meta:
        ordering = ['created',]
