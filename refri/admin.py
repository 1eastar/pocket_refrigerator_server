from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Refrigerator)
admin.site.register(models.Item)
admin.site.register(models.BasicItem)
admin.site.register(models.Memo)