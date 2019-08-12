from django.shortcuts import render
from . import serializers
from . import models
from rest_framework import generics
from django.contrib.auth.models import User

# Create your views here.

class CUserList(generics.ListCreateAPIView):
	queryset = models.CUser.objects.all()
	serializer_class = serializers.CUserSerializer

class CUserDetail(generics.RetrieveDestroyAPIView):
	queryset = models.CUser.objects.all()
	serializer_class = serializers.CUserSerializer

class AppList(generics.ListCreateAPIView):
	queryset = models.App.objects.all()
	serializer_class = serializers.AppSerializer

class AppDetail(generics.RetrieveDestroyAPIView):
	queryset = models.App.objects.all()
	serializer_class = serializers.AppSerializer

class SearchList(generics.ListCreateAPIView):
	queryset = models.Search.objects.all()
	serializer_class = serializers.SearchSerializer

class SearchDetail(generics.RetrieveDestroyAPIView):
	queryset = models.Search.objects.all()
	serializer_class = serializers.SearchSerializer