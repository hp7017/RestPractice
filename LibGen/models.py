from django.db import models

# Create your models here.

class Msg(models.Model):
	active = models.BooleanField()
	subject = models.CharField(max_length=100)
	msg = models.TextField()

	def __str__(self):
		return '{0} is {1}'.format(self.subject, self.active)

class CUser(models.Model):
	platform_choices = {
		('Desktop', 'Desktop'),
		('Mobile', 'Mobile')
	}
	status_choices = {
		('ON', 'ON'),
		('OFF', 'OFF')
	}
	uid = models.CharField(max_length=1000, primary_key=True)
	name = models.CharField(max_length=500)
	email = models.EmailField(max_length=500)
	platform = models.CharField(choices=platform_choices, max_length=20)
	version = models.CharField(max_length=10)
	status = models.CharField(choices=status_choices, max_length=10)
	msg = models.ForeignKey(Msg, related_name='users', on_delete=models.CASCADE, null=True)
	last_login = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{0} is using version-{1} on {2}'.format(self.name, self.version, self.platform)

class EnvirementVariable(models.Model):
	version = models.CharField(max_length=10)
	desktop_vesrion = models.CharField(max_length=10, help_text='If the app version does not math with it shows Update Popup')
	desktop_maintainence = models.BooleanField()
	mobile_maintainence = models.BooleanField()


	def __str__(self):
		return str('Yes' if self.id == 1 else 'Something wrong with Envirement Variable')

class AdminMsg(models.Model):
	envirement_variable = models.ForeignKey(EnvirementVariable, related_name='adminMsgs', on_delete=models.CASCADE)
	active = models.BooleanField()
	subject = models.CharField(max_length=100)
	msg = models.TextField()

	def __str__(self):
		return '{0} is {1}'.format(active, subject)

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