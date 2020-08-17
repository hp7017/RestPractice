from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import MinValueValidator
import os

# Create your models here.

class Profile(models.Model):

	def user_directory_path(self, filename):
		return 'user_{0}/{1}'.format(self.user.id, filename)

	def validate_image(fieldfile_obj):
		if get_image_dimensions(fieldfile_obj) != (180, 180):
			raise ValidationError("Profile size should be exact 180*180")

	user = models.OneToOneField(User, related_name='of_profile', on_delete=models.CASCADE)
	pic = models.ImageField(upload_to=user_directory_path, validators=[validate_image], blank=True)
	balance = models.FloatField(default=0, validators=[MinValueValidator(0)])
	phone = models.CharField(max_length=15)

class Intrest(models.Model):
	user = models.ForeignKey(User, related_name='intrests', on_delete=models.CASCADE)
	keyword = models.CharField(max_length=100)
	created_on = models.DateTimeField(auto_now_add=True)

	def clean(self):
		self.keyword = self.keyword.lower()
		super().clean()

	def __str__(self):
		return self.keyword

	class Meta:
		ordering = ['-created_on']

class Search(models.Model):
	user = models.ForeignKey(User, related_name='searchs', on_delete=models.CASCADE)
	search = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.search

class Book(models.Model):
	user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
	slug = models.SlugField(max_length=5000)
	search = models.ForeignKey(Search, related_name='books', on_delete=models.CASCADE)
	name = models.CharField(max_length=5000)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-date']

	def get_absolute_url(self):
		return reverse('books', kwargs={'slug': self.slug, 'pk': self.id})

class SponsoredBook(models.Model):

	places = (
			('Royal-Place', 'Royal Place'),
			('Search-Result', 'Search Result')
		)

	statuses = (
			('Online', 'Online'),
			('Offline', 'Offline'),
			('Insufficient-Balance', 'Insufficient Balance')
		)

	def validate_image(fieldfile_obj):
		if get_image_dimensions(fieldfile_obj) != (180, 290):
			raise ValidationError("Thumbnail should be exact 180*290")
	user = models.ForeignKey(User, related_name='sponsored_books', on_delete=models.CASCADE)

	def user_directory_path(self, filename):
		return 'user_{0}/{1}'.format(self.user.id, filename)
	
	title = models.CharField(max_length=20)
	bid = models.FloatField(validators=[MinValueValidator(5)])
	placed_on = models.CharField(choices=places, max_length=20)
	status = models.CharField(max_length=100, choices=statuses, default='Online')
	thumbnail = models.ImageField(upload_to=user_directory_path, validators=[validate_image])
	created_on = models.DateTimeField(auto_now_add=True)
	redirect_link = models.URLField(max_length=500)
	engadgements_count = models.PositiveIntegerField(default=0)
	impressions_count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.title)

	class Meta:
		ordering = ['-bid']

	def delete(self, *args, **kwargs):
		super().delete(*args, **kwargs)
		base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		path = os.path.join(base_dir, 'media', str(self.thumbnail))
		if os.path.exists(path):
			os.remove(path)
		else:
			print('already not exists')

class Keyword(models.Model):

	sponsored_book = models.ForeignKey(SponsoredBook, related_name='keywords', on_delete=models.CASCADE)
	title = models.CharField(max_length=50)

	def clean(self):
		super().clean()
		self.title = self.title.lower()
		if len(self.title.split(' ')) != 1:
			raise ValidationError({'title': 'Keyword Suppose to a single word. Please do not use spaces.'})

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

class Msg(models.Model):
	email = models.EmailField(max_length=250)
	text = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email

class Order(models.Model):
	user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
	amount = models.FloatField()
	reference_id = models.CharField(max_length=500, blank=True)
	status = models.CharField(max_length=500, default='Opened')
	payment_mode = models.CharField(max_length=500, blank=True)
	tx_msg = models.CharField(max_length=500, blank=True)
	tx_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.id}'

	class Meta:
		ordering = ['-tx_time']

class Email(models.Model):
	reply_tos = (
		('support@librarygenesis.in', 'Support'),)

	subject = models.CharField(max_length=1000)
	body = models.TextField()
	from_email = models.EmailField()
	reply_to = models.EmailField(choices=reply_tos, null=True)
	to_email = models.EmailField()

	def __str__(self):
		return f'{self.subject}'

class Proxy(models.Model):
	worked = models.BooleanField(default=False)
	ip = models.CharField(max_length=100)
	port = models.CharField(max_length=10)

	def __str__(self):
		return f'{self.ip}:{self.port} worked:{self.worked}'