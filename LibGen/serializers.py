from rest_framework import serializers
from . import models

class AppSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.App
		fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Search
		fields = '__all__'

class CUserSerializer(serializers.ModelSerializer):
	searchs = SearchSerializer(many=True, required=False, read_only=True)

	class Meta:
		model = models.CUser
		fields = ('id', 'username', 'email', 'password', 'searchs')
		extra_kwargs = {'password': {'write_only': True}}