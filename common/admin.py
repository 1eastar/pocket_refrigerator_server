from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Icon)
admin.site.register(models.Honor)
admin.site.register(models.Userdata)
admin.site.register(models.Notice)
admin.site.register(models.Barcode)
admin.site.register(models.Report)