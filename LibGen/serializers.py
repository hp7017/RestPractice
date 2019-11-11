from rest_framework import serializers
from . import models

class AppSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.App
		fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Book
		fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Search
		fields = '__all__'

class CUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.CUser
		fields = '__all__'
		extra_kwargs = {'uid': {'write_only': True}}