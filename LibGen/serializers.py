from rest_framework import serializers
from . import models

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Book
		fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
	books = BookSerializer(many=True, required=False)
	class Meta:
		model = models.Search
		fields = '__all__'

class CUserSerializer(serializers.ModelSerializer):
	searchs = SearchSerializer(many=True, required=False)
	class Meta:
		model = models.CUser
		fields = '__all__'
		extra_kwargs = {'uid': {'write_only': True}}

class MsgSerializer(serializers.ModelSerializer):
	users = CUserSerializer(many=True, required=False)
	class Meta:
		model = models.Msg
		fields = '__all__'



class AdminMsgSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AdminMsg
		fields = '__all__'

class EnvirementVariableSerializer(serializers.ModelSerializer):
	adminMsgs = AdminMsgSerializer(many=True, required=False)
	class Meta:
		model = models.EnvirementVariable
		fields = '__all__'