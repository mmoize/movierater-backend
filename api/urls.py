from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import MoviewViewSet, RatingViewSet, NewMovieViewset

router = routers.DefaultRouter()
# router.register('movies', MoviewViewSet)
router.register('ratings', RatingViewSet)

newmovie = MoviewViewSet.as_view({'post': 'create'})

app_name = 'api'

urlpatterns = [
    path('movie/', include(router.urls)),
    path('newmovie', newmovie , name='movie_create'),
          
]
