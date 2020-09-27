from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Icon)
admin.site.register(models.Honor)
admin.site.register(models.Notice)
admin.site.register(models.Barcode)
admin.site.register(models.Report)
admin.site.register(models.Food)

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'nickname',
        'email',
        'date_joined',
    )

    list_display_links = (
        'nickname',
        'email',
    )