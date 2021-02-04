from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import SleekerSerializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from core.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from account.serializers import UserSerializer
from .models import Sleeker
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

# Create your views here.
@csrf_exempt


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def CreateSleeker(request, *args, **kwargs):

    serializer = SleekerSerializers(data=request.POST )
    if serializer.is_valid(raise_exception=True):
        user = User.objects.get(id=request.POST["user"])
        serializer.save(user=user)
        return JsonResponse( serializer.data, status=201)
    return JsonResponse({}, status=400)




# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def sleekerfeed(request, *args, **kwargs):
#     qs = Sleeker.objects.all()

#     return Response(qs)

@csrf_exempt
@permission_classes([IsAuthenticated])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def sleekerfeed(request):

    if request.method == 'GET':

        qs = Sleeker.objects.all()
        serializer =  SleekerSerializers(qs, many=True)
        data = {}
        post = serializer.data




        return JsonResponse(serializer.data, safe=False)



class getPost(ModelViewSet):
    serializer_class = SleekerSerializers
    #queryset = Sleeker.objects.all()
    permission_classes = (AllowAny, )

    def get_queryset(self, *args, **kwargs):

        querysets = Sleeker.objects.all()
  

        return querysets
