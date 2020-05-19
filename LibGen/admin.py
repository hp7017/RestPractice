from django.contrib import admin
from . import models

# Register your models here.

class BookInline(admin.TabularInline):
	model = models.Book

class SearchInline(admin.TabularInline):
	model = models.Search

class MsgInline(admin.TabularInline):
	model = models.Msg

class CuserAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'last_login']
	list_filter = ('status', 'created', 'last_login', 'version', 'platform')
	list_display = ('name', 'version', 'status', 'last_login', 'platform')
	inlines = [SearchInline]
	actions=['mark_off', 'send_msgs']

	def mark_off(self, request, queryset):
		queryset.update(status='OFF')
	mark_off.short_description = "Mark selected user as OFF"

	def send_msgs(self, request, queryset):
		active_messages = models.Msg.filter(active=True)
		for active_message in active_messages:
			for user in queryset:
				active_message.users.add(user)
	send_msgs.short_description = 'Send messages to selected users'

class SearchAdmin(admin.ModelAdmin):
	readonly_fields = ['date']
	list_display = ['search', 'user', 'date']
	list_filter = ['date']
	inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
	readonly_fields = ['date']
	list_display = ['name', 'search', 'date']
	list_filter = ['date']

admin.site.register(models.EnvirementVariable)
admin.site.register(models.Msg)
admin.site.register(models.AdminMsg)
admin.site.register(models.Search, SearchAdmin)
admin.site.register(models.CUser, CuserAdmin)
admin.site.register(models.Book, BookAdmin)