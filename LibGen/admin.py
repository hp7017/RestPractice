from django.contrib import admin
from . import models

# Register your models here.

class BookInline(admin.TabularInline):
	model = models.Book

class SearchInline(admin.TabularInline):
	model = models.Search

class CUserInline(admin.TabularInline):
	model = models.CUser
	readonly_fields = ['name', 'email']
	fields = ['name', 'email']

class CuserAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'last_login']
	list_filter = ('status', 'created', 'last_login', 'version')
	list_display = ('name', 'status', 'last_login')
	inlines = [SearchInline]
	actions = ['add_receiver']

	def add_receiver(self, request, users):
		active_msgs = models.Msg.objects.filter(active=True)
		for active_msg in active_msgs:
			for user in users:
				active_msg.users.add(user)
	add_receiver.short_description = 'Add selected users to receiver for active msgs'

class SearchAdmin(admin.ModelAdmin):
	readonly_fields = ['id']
	list_display = ['search', 'user', 'date']
	list_filter = ['date']
	inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
	list_display = ['name', 'search', 'date']
	list_filter = ['date']

class AdminMsgAdmin(admin.ModelAdmin):
	list_display = ['subject', 'active']

class MsgAdmin(admin.ModelAdmin):
	list_display = ['subject', 'active']
	inlines = [CUserInline]

admin.site.register(models.EnvirementVariable)
admin.site.register(models.Msg, MsgAdmin)
admin.site.register(models.AdminMsg, AdminMsgAdmin)
admin.site.register(models.Search, SearchAdmin)
admin.site.register(models.CUser, CuserAdmin)
admin.site.register(models.Book, BookAdmin)