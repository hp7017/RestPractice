from rest_framework import serializers
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User

class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
	votes = VoteSerializer(many=True, required=False, read_only=True)

	class Meta:
		model = Choice
		fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
	choices = ChoiceSerializer(many=True, required=False, read_only=True)

	class Meta:
		model = Poll
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	polls = PollSerializer(many=True, required=False, read_only=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'polls')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			email = validated_data['email'],
			username = validated_data['username'])
		user.set_password(validated_data['password'])
		user.save()
		return user