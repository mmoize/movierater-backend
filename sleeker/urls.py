from django.urls import path
from .views import CreateSleeker, sleekerfeed, getPost



app_name = "sleeker"

getlist = getPost.as_view({'get': 'list'})


urlpatterns = [
    path('create/',CreateSleeker),
    path('get',sleekerfeed),
     path('getlist', getlist , name='getlist'),
]
