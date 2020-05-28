from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subscriber(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Msg(models.Model):
	subscriber = models.ForeignKey(Subscriber, related_name='msgs', on_delete=models.CASCADE)
	subject = models.CharField(max_length=500)
	content = models.TextField() 


class Search(models.Model):
	user = models.ForeignKey(User, related_name='searchs', on_delete=models.CASCADE)
	search = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.search

class Book(models.Model):
	user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
	search = models.ForeignKey(Search, related_name='books', on_delete=models.CASCADE)
	name = models.CharField(max_length=5000)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-date']