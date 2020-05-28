from django.contrib import admin
from . import models

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
	list_display = ['name', 'search', 'date']
	list_filter = ['date']

class SubscriberAdmin(admin.ModelAdmin):
	list_filter = ['created_on']
	inlines = [MsgInline]

admin.site.register(models.Msg)
admin.site.register(models.Subscriber, SubscriberAdmin)
admin.site.register(models.Search, SearchAdmin)
admin.site.register(models.Book, BookAdmin)