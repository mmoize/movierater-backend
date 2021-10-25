from rest_framework import serializers
from .models import Movie, Movierating, Review, Comment
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from account.serializers import UserSerializer
from django.forms import ImageField as DjangoImageField



class MovieSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name="movie:movie-detail", read_only=True, lookup_field="id")
    class Meta:
        model = Movie
        fields = [
            'id','url', 'title', 
            'plot', 'poster', 'director', 
            'released', 'year', 'genre', 
            'imdbid', 'runtime','no_of_ratings', 'avg_rating']


    def create(self, validated_data):

        data = self.context['movie_info']

        
        movie_obj = Movie.objects.get_or_create(
            title = data["title"],
            plot = data['plot'],
            poster = data['poster'],
            director = data['director'],
            released = data['released'],
            year = data['year'],
            genre = data['genre'],
            imbdid = data['imbdid'],
            runtime = data['runtime']
        )


        movie_instance = movie_obj[0]
        return movie_instance


class Movie_RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movierating
        fields = ['id', 'stars', 'user', 'movie']



class MovieReviewSerializer(serializers.HyperlinkedModelSerializer):
    movie = serializers.HyperlinkedRelatedField(view_name="movie:movie-detail", read_only=True, source="movie_id")
    user = UserSerializer(read_only=True)
    url = serializers.HyperlinkedRelatedField(view_name="movie:review-detail", read_only=True, lookup_field="id")
    class Meta:
        model = Review
        fields = ['id','url', 'movie', 'user', 'review_body']
