from django.contrib import admin
from . import models

# Register your models here.

class BookInline(admin.TabularInline):
	model = models.Book

class SearchInline(admin.TabularInline):
	model = models.Search

class CuserAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'last_login']
	list_filter = ('status', 'created', 'last_login', 'version')
	list_display = ('name', 'status', 'last_login')
	inlines = [SearchInline]

class SearchAdmin(admin.ModelAdmin):
	list_display = ['search', 'user', 'date']
	list_filter = ['date']
	inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
	list_display = ['name', 'search', 'date']
	list_filter = ['date']

admin.site.register(models.App)
admin.site.register(models.Search, SearchAdmin)
admin.site.register(models.CUser, CuserAdmin)
admin.site.register(models.Book, BookAdmin)