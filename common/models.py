from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from rest_framework.authtoken.models import Token

import datetime

# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Refrigerator = apps.get_model('refri', 'Refrigerator')
        Refrigerator.objects.create(user=instance)


class Icon(models.Model):
    name = models.CharField(default='', max_length=20)
    image = models.ImageField(upload_to="icon", null=True, blank=True)     # MEDIA_ROOT/icon/파일명.png 

    def __str__(self):
        return self.name


class Honor(models.Model):
    name = models.CharField(default='', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.CASCADE)
    icon = models.ForeignKey(Icon, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Userdata(models.Model):
    nickname = models.CharField(max_length=10, blank=True)          # default = username 설정 어떻게?
    report_num = models.IntegerField(default=0)
    gender = models.IntegerField(default=0)
    birth = models.CharField(max_length=4, default='0000')
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    # recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    main_honor = models.ForeignKey(Honor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "userdata of #{}".format(self.nickname)


class Notice(models.Model):
    post_type = models.IntegerField(default=0)  # 0: 공지사항, 1: FAQ
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=True)
    visit_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to="", null=True, blank=True)     # file url 설정 (upload_to)
    file = models.FileField(upload_to="", null=True, blank=True)     # file url 설정 (upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Barcode(models.Model):
    barcode_num = models.CharField(default='0000000000000', max_length=13, null=False)
    # barcode_data = ArrayField(ArrayField(models.CharField(), size=20), size=100000)
    # array model ????????
    item_name = models.CharField(max_length=50)
    item_category = models.CharField(max_length=20, default="")
    item_dday = models.IntegerField(null=False)
    item_ddate = models.DateField(default=datetime.date.today)

    item = models.ForeignKey('refri.Item', on_delete=models.CASCADE, null=True, blank=True)
    basicitem = models.ForeignKey('refri.BasicItem', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.item_name


class Report(models.Model):
    report_type = models.IntegerField(default=-1)    # 0: user, 1: recipe, 2: comment
    report_object_id = models.IntegerField(default=-1)
    report_category = models.IntegerField(default=-1)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return "Recipe #{}".format(self.recipe.id)