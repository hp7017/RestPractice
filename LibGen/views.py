from . import serializers
from . import models
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

# Create your views here.

class CreateBook(APIView):
	serializer_class = serializers.BookSerializer

	def post(self, request, user_pk, search_pk):
		data = {'search':search_pk, 'name':request.data.get('name')}
		book_serializer = serializers.BookSerializer(data=data)
		if book_serializer.is_valid():
			book_serializer.save()
			return Response(book_serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateSearch(APIView):	
	serializer_class = serializers.SearchSerializer

	def post(self, request, user_pk):
		data = {'search':request.data.get('search'), 'user':user_pk}
		search_serializer = serializers.SearchSerializer(data=data)
		if search_serializer.is_valid():
			search_serializer.save()
			return Response(search_serializer.data, status.HTTP_201_CREATED)
		else:
			return Response(search_serializer.errors, status.HTTP_400_BAD_REQUEST)

class CreateUser(generics.CreateAPIView):
	serializer_class = serializers.CUserSerializer




class ReadEnvirementVariable(generics.RetrieveAPIView):
	queryset = models.EnvirementVariable.objects.all()
	serializer_class = serializers.EnvirementVariableSerializer