from django.urls import path
from .views import CreateSleeker, sleekerfeed



app_name = "sleeker"


urlpatterns = [
    path('create/',CreateSleeker),
    path('get',sleekerfeed)
]
