from django.contrib import admin
from .models import Movie, Rating, MoviesImage

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(MoviesImage)
