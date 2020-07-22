from django.db import models
from django.conf import settings


# Create your models here.

class Refrigerator(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_num = models.IntegerField(default=0)
    basic_item_num = models.IntegerField(default=0)
    memo_num = models.IntegerField(default=0)
    cool_refrige_item_num = models.IntegerField(default=0)
    freeze_refrige_item_num = models.IntegerField(default=0)
    room_temp_item_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # memo = models.ForeignKey(Memo, on_delete=models.CASCADE)
    # basicItem = models.ManyToManyField(BasicItem)
    # item = models.ManyToManyField(Item);

    def __str__(self):
        return "{}의 냉장고".format(self.user.username)

class Item(models.Model):
    position = models.IntegerField(default=0) # 냉장, 냉동, 실온
    dday = models.IntegerField(default=0)
    ddate = models.CharField(max_length=8, default='00.00.00')
    name = models.CharField(default='', max_length=50)
    category = models.CharField(default='', max_length=20)
    user_comment = models.TextField()
    amount = models.IntegerField(default=0) # 개수
    unit = models.CharField(max_length=1, default='개')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    create_type = models.IntegerField(default=-1) # 0: 바코드, 1: 직접입력
    exist = models.BooleanField(default=False)
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    icon = models.ForeignKey('common.Icon', null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return "Item : {}".format(self.name)

class BasicItem(models.Model):
    name = models.CharField(default='', max_length=20)
    position = models.IntegerField(default=0) # 냉장, 냉동, 실온
    user_comment = models.TextField(max_length=200)
    exist = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    icon = models.ForeignKey('common.Icon', null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return "Basic Item : {}".format(self.name)


class Memo(models.Model):
    color = models.CharField(max_length=7, default='#fff44f')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE)

    def __str__(self):
        return "냉장고 #{} 메모".format(self.refrigerator.pk)
    
