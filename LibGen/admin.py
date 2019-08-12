from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.App)
admin.site.register(models.Search)
admin.site.register(models.CUser)