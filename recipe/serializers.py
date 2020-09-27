from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from django.conf import settings

from . import models
# from refri.models import Item, BasicItem
from common.serializers import IconSerializer
from refri.serializers import ItemSerializer, BasicItemSerializer


# class IconSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = 'common.Icon'
#         fields = ('pk', 'name', 'image')

# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = 'refri.Item'
#         fields = ('pk', 'author', 'name', 'icon', 'user_comment', 'position', 'amount', 'dday', 'ddate', 'category', 'exist', 'create_type', 'created_at', 'updated_at')

# class BasicItemSerializer(serializers.ModelSerializer):
#     icon = IconSerializer(many=False, read_only=True)
#     class Meta:
#         model = 'refri.BasicItem'
#         fields = ('pk', 'author', 'name', 'icon', 'user_comment', 'position', 'exist', 'created_at', 'updated_at')


class RecipeItemSerializer(serializers.ModelSerializer):
    # item_set = ItemSerializer(many=True, read_only=True)
    # basicitem_set = BasicItemSerializer(many=True, read_only=True)
    item_set = serializers.SerializerMethodField()
    basicitem_set = serializers.SerializerMethodField()
    class Meta:
        model = models.RecipeItem
        fields = ('pk', 'item_set', 'basicitem_set', 'amount', 'recipe')
        # fields = '__all__'

    def get_item_set(self, obj):
        item = obj.item
        if item == None:
            return
        return ItemSerializer(item).data

    def get_basicitem_set(self, obj):
        basicitem = obj.basic_item
        if basicitem == None:
            return
        return BasicItemSerializer(basicitem).data


class CommentSerializer(serializers.ModelSerializer):
    # author_id = ReadOnlyField(source='author.id')
    # author_data = UserdataSerializer(many=False, read_only=True)
    # author = serializers.SerializerMethodField()
    class Meta:
        model = models.Comment
        # fields = ('author_data', 'content', 'report_num', 'recipe', 'created_at', 'updated_at')
        fields = '__all__'
    def get_author(self, obj):
        from common.serializers import UserSerializer
        user = self.get_author(obj)
        return UserSerializer(user, many=False, read_only=True).data

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    # recipe_items = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True, read_only=True)
    tag_set = TagSerializer(many=True, read_only=True)
    class Meta:
        model = models.Recipe
        fields = ('pk', 'author', 'name', 'content', 'author_comment', 'tag_set', 'comment_set', 'like_num', 'comment_num', 'created_at', 'updated_at')

    def get_recipe_items(self, obj):
        recipe_item_query_set = models.RecipeItem.objects.filter(recipe=obj)
        return RecipeItemSerializer(recipe_item_query_set, many=True).data


class UserRecipeStoreSerializer(serializers.ModelSerializer):
    recipe_set = RecipeSerializer(many=True, read_only=True)
    class Meta:
        model = models.UserRecipeStore
        fields = ('pk', 'user', 'recipe_set', 'created_at', 'updated_at')

class UserRecipeHistorySerializer(serializers.ModelSerializer):
    recipe_set = RecipeSerializer(many=True, read_only=True)
    class Meta:
        model = models.UserRecipeHistory
        fields = ('pk', 'user', 'recipe_set', 'created_at', 'updated_at')


class RecipeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'common.Report'
        fields = '__all__'
