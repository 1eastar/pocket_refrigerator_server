from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from rest_framework.authtoken.models import Token

import datetime

# Create your models here.

class Icon(models.Model):
    name = models.CharField(default='', max_length=20)
    image = models.ImageField(upload_to="icon", null=True, blank=True)     # MEDIA_ROOT/icon/파일명.png 

    def __str__(self):
        return self.name



class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, nickname, password=None, gender=0, birth='2020', icon=1):        
        if not email:
            raise ValueError('must have user email')
        icon_instance = get_object_or_404(Icon, id=icon)
        user = self.model(
            email = self.normalize_email(email),            
            nickname = nickname,
            gender = gender,
            birth = birth,
            icon = icon_instance,
        )
        user.set_password(password)  
        user.save(using=self._db)        
        return user  

    def create_superuser(self, email, nickname, password, gender=0, birth='2020', icon=1):        
        user = self.create_user(            
            email = self.normalize_email(email),            
            nickname = nickname,            
            password = password,
            gender = gender,
            birth = birth,
            icon = icon,
        )        
        user.is_admin = True        
        user.is_superuser = True 
        user.save(using=self._db)        
        return user 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(        
        max_length=255,        
        unique=True,    
    )
    nickname = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )
    gender = models.IntegerField(default=0)
    birth = models.CharField(max_length=4, default='0000')
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)
    report_num = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)     
    date_joined = models.DateTimeField(auto_now_add=True)     
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['nickname', 'gender', 'birth', 'icon']

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Refrigerator = apps.get_model('refri', 'Refrigerator')
        Refrigerator.objects.create(user=instance)


class Honor(models.Model):
    name = models.CharField(default='', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.CASCADE)
    icon = models.ForeignKey(Icon, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

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
    author_id = models.IntegerField(default=-1)
    report_type = models.IntegerField(default=-1)    # 0: user, 1: recipe, 2: comment
    # report_object_id = models.IntegerField(default=-1, null=True, blank=True)
    report_category = models.IntegerField(default=-1)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.PROTECT, null=True, blank=True)
    comment = models.ForeignKey('recipe.Comment', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        if self.report_type == 0:
            return "User #{}".format(self.user.id)
        if self.report_type == 1:
            return "Recipe #{}".format(self.recipe.id)
        if self.report_type == 2:
            return "Comment #{}".format(self.comment.id)


class Food(models.Model):
    BAR_CD = models.CharField(default='0000000000000', max_length=50)
    PRDLST_DCNM = models.CharField(default='category', max_length=50, null=True, blank=True)
    PRDLST_NM = models.CharField(default='name', max_length=50, null=True, blank=True)
    BSSH_NM = models.CharField(default='corp', max_length=50, null=True, blank=True)
    PRMS_DT = models.CharField(default='make start date', max_length=50, null=True, blank=True)
    CLSBIZ_DT = models.CharField(default='', max_length=50, null=True, blank=True)
    INDUTY_NM = models.CharField(default='corp category', max_length=50, null=True, blank=True)
    SITE_ADDR = models.CharField(default='address', max_length=50, null=True, blank=True)
    POG_DAYCNT = models.CharField(default='shelf life', max_length=50, null=True, blank=True)
    END_DT = models.CharField(default='make finish date', max_length=50, null=True, blank=True)
    PRDLST_REPORT_NO = models.CharField(default='report number', max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.PRDLST_NM
