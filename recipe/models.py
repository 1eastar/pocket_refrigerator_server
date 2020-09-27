from django.db import models
from django.conf import settings

from common.models import User

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(default='', max_length=50)
    content = models.TextField()
    author_comment = models.TextField()
    like_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    store_num = models.IntegerField(default=0)
    report_num = models.IntegerField(default=0)
    visit_num = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)    # author

    # items = models.ManyToManyField(Item)
    # basicItems = models.ManyToManyField(BasicItem)

    def __str__(self):
        return self.name

class UserRecipeStore(models.Model):    # 유저별 찜한 레시피
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserRecipeHistory(models.Model):      # 유저별 사용한 레시피 히스토리
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RecipeItem(models.Model):
    # items = models.ManyToManyField(Item)
    # basicitems = models.ManyToManyField(BasicItem)
    amount = models.IntegerField(default=0)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    item = models.ForeignKey('refri.Item', on_delete=models.CASCADE, null=True, blank=True)
    basic_item = models.ForeignKey('refri.BasicItem', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{}의 재료".format(self.recipe.name)


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return "#{}, Like recipe #{}".format(self.pk, self.recipe.pk)


class Comment(models.Model):
    content = models.TextField(max_length=500)
    report_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Tag(models.Model):
    name = models.CharField(max_length=50)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
