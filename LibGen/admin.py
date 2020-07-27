from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from . import models
import json
from datetime import datetime

# Register your models here.
class BookInline(admin.StackedInline):
	model = models.Book

class SearchInline(admin.TabularInline):
	model = models.Search

class KeywordInline(admin.TabularInline):
	model = models.Keyword

class ProfileInline(admin.TabularInline):
	model = models.Profile

class ToReceiverInline(admin.TabularInline):
	model = models.ToReceiver

class CCReceiverInline(admin.TabularInline):
	model = models.CCReceiver

class ReplyToInline(admin.TabularInline):
	model = models.ReplyTo



class CustomUserAdmin(UserAdmin):
	actions = ['add_users_from_json']
	list_display = ['id', 'username', 'email', 'date_joined']
	inlines = [ProfileInline]

	def add_users_from_json(self, request, queryset):
		with open('cuser_data.json') as file:
			data = json.load(file)
			for key, value in data.items():
				user = models.User()
				user.username = key
				user.set_password(key)
				user.email = value['email']
				user.first_name = value['name']
				user.date_joined = datetime.strptime(value['created'], "%Y-%m-%d %H:%M:%S.%f+00:00")
				user.save()
				print(user)

class SearchAdmin(admin.ModelAdmin):
	list_display = ['search', 'user', 'date']
	list_filter = ['date']
	inlines = [BookInline]
	actions = ['delete_all_searches_of_testing_user']

	def delete_all_searches_of_testing_user(self, request, queryset):
		models.Search.objects.filter(user_id=3301).delete()

class BookAdmin(admin.ModelAdmin):
	readonly_fields = ['id']
	list_display = ['name', 'user', 'search', 'date']
	# list_filter = ['date']
	actions = ['delete_text_after_number', 'add_slug_from_name']

	def delete_text_after_number(self, request, queryset):
		books = models.Book.objects.all()
		for book in books:
			index = None
			stop_at_alpha = True
			for i, ch in enumerate(book.name[-1:0:-1]):
				if ch == ']':
					stop_at_alpha = False
				elif stop_at_alpha and ch.isalpha():
					index = len(book.name)-i
					print(str(i), ch)
					break
				elif ch == '[':
					index = len(book.name)-i
					print(str(i), ch)
					break
			if index:
				new_name = book.name[:index-1]
				book.name = new_name
				book.save()
				
	non_url_safe = ['"', '#', '$', '%', '&', '+',
					',', '/', ':', ';', '=', '?',
					'@', '[', '\\', ']', '^', '`',
					'{', '|', '}', '~', "'"]

	def slugify(self, text):
		"""
		Turn the text content of a header into a slug for use in an ID
		"""
		non_safe = [c for c in text if c in self.non_url_safe]
		if non_safe:
			for c in non_safe:
				text = text.replace(c, '')
		# Strip leading, trailing and multiple whitespace, convert remaining whitespace to _
		text = u'-'.join(text.split())
		return text

	def add_slug_from_name(self, request, queryset):
		books = models.Book.objects.all()
		total = books.count()
		for i, book in enumerate(books):
			book.slug = self.slugify(book.name)
			book.save()
			print(f'{i}/{total}')


		

class SponsordedBookAdmin(admin.ModelAdmin):
	list_display = ['title', 'user', 'bid', 'impressions_count', 'engadgements_count', 'status']
	inlines = [KeywordInline]

class KeywordAdmin(admin.ModelAdmin):
	list_display = ['title', 'sponsored_book']

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'balance']

class IntrestAdmin(admin.ModelAdmin):
	list_display = ['keyword', 'user']

class MsgAdmin(admin.ModelAdmin):
	readonly_fields = ['id']
	list_display = ['id', 'email', 'text', 'created_on']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'amount', 'status', 'tx_time', 'user']

class EmailAdmin(admin.ModelAdmin):
	list_display = ['subject', 'from_email', 'subject']
	inlines = [ToReceiverInline, CCReceiverInline, ReplyToInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Search, SearchAdmin)
admin.site.register(models.Intrest, IntrestAdmin)
admin.site.register(models.Keyword, KeywordAdmin)
admin.site.register(models.SponsoredBook, SponsordedBookAdmin)
admin.site.register(models.Evaluation)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Msg, MsgAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Email, EmailAdmin)