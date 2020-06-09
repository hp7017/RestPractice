from django.contrib import admin
from . import models
import json

# Register your models here.

class BookInline(admin.TabularInline):
	model = models.Book

class SearchInline(admin.TabularInline):
	model = models.Search

class MsgInline(admin.TabularInline):
	model = models.Msg

class SearchAdmin(admin.ModelAdmin):
	list_display = ['search', 'date']
	list_filter = ['date']
	inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
	readonly_fields = ['id']
	list_display = ['name', 'search', 'date']
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

admin.site.register(models.Msg)
admin.site.register(models.Subscriber, SubscriberAdmin)
admin.site.register(models.Search, SearchAdmin)
admin.site.register(models.Book, BookAdmin)