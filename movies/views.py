from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Movierating, Review, Comment
from .serializers import MovieSerializer, Movie_RatingSerializer, MovieReviewSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAcceptable
from .utils import MultipartJsonParser
from rest_framework.parsers import JSONParser



class MoviewViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    parser_classes = [MultipartJsonParser, JSONParser]
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )


    def get_serializer_context(self):
        context = super(MoviewViewSet, self).get_serializer_context()
 
        if len(self.request.data) > 0:
            context.update({
               'included_images': self.request.FILES
            })
            context.update({
                'movie_info': self.request.data
            })

        return context

    def create(self, request, *args, **kwargs):
    
        try:
            pass
        except Exception:
            raise NotAcceptable(

                detail={
                    'message': 'upload a valid image. The file you uploaded was '
                                'neither not an image or a corrupted image.'
                }, code=406
            )
        print('this is new request data', request.data)
        serializer = self.get_serializer(data=request.data)
        
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            
            try:
                rating =Movierating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = Movie_RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status= status.HTTP_200_OK)
            except:
                rating = Movierating.objects.create(user=user, movie=movie, stars=stars)
                serializer = Movie_RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status= status.HTTP_200_OK)

            
        else:
            response = {'message': 'you need to provide stars'}
            return Response(response, status= status.HTTP_400_BAD_REQUEST)