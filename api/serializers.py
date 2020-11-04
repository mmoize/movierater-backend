from rest_framework import serializers
from .models import Movie, Rating, MoviesImage
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from account.serializers import UserSerializer
from django.forms import ImageField as DjangoImageField




class Movies_ImageSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name="api:moviesimage-detail", read_only=True, lookup_field="moviesimage")
    movie = serializers.HyperlinkedRelatedField(view_name="api:movie-detail", read_only=True, source="movie_user")
    #movie_id = serializers.CharField(source='movie_id', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = MoviesImage
        fields =['id', 'movie','url', 'image', 'created', 'user']
        extra_kwargs = { 
            'movie': {'required': False},
            'movie_id': {'required': False},
            #'url': {'view_name': 'api:moviesimage-detail'}, 
        }



class MoviesImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name="api:moviesimage-detail", read_only=True, lookup_field="moviesimage")
    movie = serializers.HyperlinkedRelatedField(view_name="api:movie-detail", read_only=True, source="user_movie")
    #movie_id = serializers.CharField(source='movie_id', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = MoviesImage
        fields =['id', 'movie','url', 'image', 'created', 'user']
        extra_kwargs = { 
            'movie': {'required': False},
            'movie_id': {'required': False},
            'url': {'view_name': 'api:moviesimage-detail'}, 
        }
 
    
    def validate(self, attrs):
    
        default_error_messages = {
            'invalid_image':
            'Upload a valid image. The file you uploaded was either not an image'
        }

        for i in self.initial_data.getlist('image'):
            print('this is imgData', i)
            django_field = DjangoImageField()
            django_field.error_messages = default_error_messages
            django_field.clean(i)
        return attrs




class MovieSerializer(serializers.HyperlinkedModelSerializer):
    moviesimage_set = Movies_ImageSerializer(allow_null=True, many=True, read_only=True)
    user = UserSerializer(read_only=True)
    url = serializers.HyperlinkedRelatedField(view_name="api:movie-detail", read_only=True, lookup_field="user")
    class Meta:
        model = Movie
        fields = ['id','url', 'user', 'title', 'moviesimage_set', 'description', 'no_of_ratings', 'avg_rating']

    def create(self, validated_data):
        print("another", self.context['included_images'] )
        data = self.context['movie_info']
        movie_title = data['title']
        movie_description = data['description']
        #movie_description = data['image']
        
        currentUser = User.objects.get(id=self.context['request'].user.id)
        
        movie_obj = Movie.objects.get_or_create(
            title = movie_title,
            description = movie_description,
            user = currentUser
        )

        images_data = self.context['included_images']
        movie_instance = movie_obj[0]
        print('its instance movie', movie_instance)
        for i in images_data.getlist('image'):
            print("another", i)
            MoviesImage.objects.create(movie=movie_instance, image=i,  user=self.context['request'].user)
        print('its done', movie_obj)
        return movie_instance

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'stars', 'user', 'movie']

