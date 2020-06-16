
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

# Create your models here.

class Intrest(models.Model):
	user = models.ForeignKey(User, related_name='intrests', on_delete=models.CASCADE)
	keyword = models.CharField(max_length=100)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.keyword

	class Meta:
		ordering = ['-created_on']

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

	def __str__(self):
		return self.subject


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

	def get_absolute_url(self):
		return reverse('books', kwargs={'pk': self.id})

class SponsoredBook(models.Model):

	places = (
			('Royal Place', 'Royal Place'),
			('Search Result', 'Search Result')
		)

	def validate_image(fieldfile_obj):
		if get_image_dimensions(fieldfile_obj) != (180, 290):
			raise ValidationError("Thumnail should be exact 180*290")
	user = models.ForeignKey(User, related_name='sponsored_books', on_delete=models.CASCADE)

	def user_directory_path(self, filename):
		return 'media/user_{0}/{1}'.format(self.user.id, filename)
	
	title = models.CharField(max_length=20)
	bid = models.FloatField()
	placed_on = models.CharField(choices=places, max_length=20)
	description = models.TextField()
	height = models.PositiveIntegerField()
	width = models.PositiveIntegerField()
	verified = models.BooleanField(default=False)
	thumbnail = models.ImageField(upload_to=user_directory_path, height_field='height', width_field='width', validators=[validate_image])
	created_on = models.DateTimeField(auto_now_add=True)
	redirect_link = models.URLField(max_length=500)

	def __str__(self):
		return str(self.title)

	class Meta:
		ordering = ['-bid']

class Keyword(models.Model):

	sponsored_book = models.ForeignKey(SponsoredBook, related_name='keywords', on_delete=models.CASCADE)
	title = models.CharField(max_length=50, unique=True)

	def clean(self):
		self.title = self.title.lower()

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['title']

class Evaluation(models.Model):
	user = models.ForeignKey(User, related_name='evaluations', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, related_name='evaluations', on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	link = models.URLField()

	def __str__(self):
		return self.title