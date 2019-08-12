from django.db import models

# Create your models here.

class CUser(models.Model):
	username = models.CharField(max_length=500)
	email = models.EmailField()
	password = models.CharField(max_length=500)

	def __str__(self):
		return self.username

class App(models.Model):
	update = models.BooleanField(default=False)

	def __str__(self):
		return str(self.update)

class Search(models.Model):
	user = models.ForeignKey(CUser, related_name='searchs', on_delete=models.CASCADE)
	search = models.CharField(max_length=500)

	def __str__(self):
		return self.search