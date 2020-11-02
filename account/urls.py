from django.urls import path, include

from .views import CustomAuthTokenSignup, CustomAuthTokenLogin

from rest_framework import routers


router = routers.DefaultRouter()


app_name = 'account'

urlpatterns = [
    path('signup', CustomAuthTokenSignup.as_view()),
    path('login', CustomAuthTokenLogin.as_view()),
    path('api/', include(router.urls)),
    #path('users', UserRegisViewSet.as_view(), name="user_registration"),
]