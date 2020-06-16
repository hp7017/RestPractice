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

class CustomUserAdmin(UserAdmin):
	actions = ['add_users_from_json']
	list_display = ['username', 'email', 'date_joined']

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

class MsgInline(admin.TabularInline):
	model = models.Msg

class SearchAdmin(admin.ModelAdmin):
	list_display = ['search', 'user', 'date']
	list_filter = ['date']
	inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
	readonly_fields = ['id']
	list_display = ['name', 'user', 'search', 'date']
	list_filter = ['date']
	actions = ['delete_text_after_number']

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

class SubscriberAdmin(admin.ModelAdmin):
	list_filter = ['created_on']
	inlines = [MsgInline]

class SponsordedBookAdmin(admin.ModelAdmin):
	readonly_fields = ['height', 'width', 'thumbnail']
	list_display = ['title', 'user', 'bid', 'verified']
	inlines = [KeywordInline]

class KeywordAdmin(admin.ModelAdmin):
	list_display = ['title', 'sponsored_book']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(models.Msg)
admin.site.register(models.Subscriber, SubscriberAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Search, SearchAdmin)
admin.site.register(models.Intrest)
admin.site.register(models.Keyword, KeywordAdmin)
admin.site.register(models.SponsoredBook, SponsordedBookAdmin)
admin.site.register(models.Evaluation)