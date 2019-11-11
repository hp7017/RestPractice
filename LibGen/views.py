from . import serializers
from . import models
from rest_framework import generics

# Create your views here.

class AppDetail(generics.RetrieveAPIView):
	queryset = models.App.objects.all()
	serializer_class = serializers.AppSerializer

class CUserList(generics.CreateAPIView):
	serializer_class = serializers.CUserSerializer

class CUserDetail(generics.RetrieveUpdateAPIView):
	queryset = models.CUser.objects.all()
	serializer_class = serializers.CUserSerializer

class SearchList(generics.CreateAPIView):	
	serializer_class = serializers.SearchSerializer

class BookList(generics.CreateAPIView):
	serializer_class = serializers.BookSerializer