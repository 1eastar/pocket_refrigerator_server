from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from django.conf import settings

from . import models


class IconSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Icon
        fields = ('pk', 'name', 'image')

class HonorSerializer(serializers.ModelSerializer):
    honor_icon = IconSerializer(many=False, read_only=False)
    class Meta:
        model = models.Honor
        fields = ('pk', 'name', 'created_at', 'honor_icon')


class UserdataSerializer(serializers.ModelSerializer):
    # honors = ReadOnlyField(source='userdata.honor')
    main_honor = HonorSerializer(many=False, read_only=False, required=False)
    class Meta:
        model = models.Userdata
        fields = ('pk', 'nickname', 'report_num', 'main_honor')

class AuthSerializer(serializers.ModelSerializer):
    userdata = UserdataSerializer(many=False, read_only=False, required=False)
    # userdata = ReadOnlyField(source='userdata')
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('pk', 'username', 'email', 'userdata')



class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notice
        fields = ('pk', 'post_type', 'title', 'content', 'visit_count', 'image', 'file', 'created_at', 'updated_at')

class BarcodeSerializer(serializers.ModelSerializer):
    # item = serializers.ItemSerializer(many=True, read_only=True, required=False)
    # basicitem = serializers.BasicItemSerializer(many=True, read_only=True, required=False)
    # item = serializers.SerializerMethodField(required=False)
    # basicitem = serializers.SerializerMethodField(required=False)
    class Meta:
        model = models.Barcode
        # fields = ('barcode_num', 'item_name', 'item_category', 'item_dday', 'item_ddate', 'item', 'basicitem')
        fields = '__all__'

    def get_item(self, obj):
        from recipe.serializers import ItemSerializer
        return  ItemSerializer(obj, many=True, read_only=True, required=False).data
    
    def get_basicitem(self, obj):
        from recipe.serializers import BasicItemSerializer
        return BasicItemSerializer(obj, many=True, read_only=True, required=False).data


class ReportSerializer(serializers.ModelSerializer):
    author = AuthSerializer(many=False, read_only=True)
    class Meta:
        model = models.Report
        fields = ('pk', 'author', 'recipe', 'report_type', 'report_object_id', 'report_category', 'content', 'created_at', 'updated_at')