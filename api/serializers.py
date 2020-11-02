from rest_framework import serializers
from .models import Movie, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'no_of_ratings', 'avg_rating', 'image']

        def create(self, validated_data):
            data = self.context['movie_info']
            movie_title = data['title']
            movie_description = data['description']
            #movie_description = data['image']

            movie_obj = Movie.objects.get_or_create(
                title = movie_title,
                description = movie_description
            )

            return movie_obj

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'stars', 'user', 'movie']

