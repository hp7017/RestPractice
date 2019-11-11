from django.db import models

# Create your models here.

class CUser(models.Model):
	choices = {
		(1, 'ON'),
		(0, 'OFF')
	}
	uid = models.CharField(max_length=1000, primary_key=True)
	name = models.CharField(max_length=500)
	email = models.EmailField(max_length=500)
	version = models.CharField(max_length=10)
	status = models.CharField(choices=choices, max_length=10)
	last_login = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.uid

class App(models.Model):
	version = models.CharField(max_length=10)

	def __str__(self):
		return str(self.version)

class Search(models.Model):
	user = models.ForeignKey(CUser, related_name='searchs', on_delete=models.CASCADE)
	search = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.search

class Book(models.Model):
	search = models.ForeignKey(Search, related_name='books', on_delete=models.CASCADE)
	name = models.CharField(max_length=5000)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name