from django.shortcuts import get_object_or_404
from rest_framework import generics

from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User

# Create your views here.

class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class PollList(generics.ListCreateAPIView):
	queryset = Poll.objects.all()
	serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
	queryset = Poll.objects.all()
	serializer_class = PollSerializer

class ChoiceList(generics.ListCreateAPIView):
	queryset = Choice.objects.all()
	serializer_class = ChoiceSerializer

class ChoiceDetail(generics.RetrieveDestroyAPIView):
	queryset = Choice.objects.all()
	serializer_class = ChoiceSerializer

class VoteList(generics.ListCreateAPIView):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer

class VoteDetail(generics.RetrieveDestroyAPIView):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer