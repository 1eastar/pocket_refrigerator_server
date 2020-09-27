from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from django.conf import settings

from . import models
from common.serializers import IconSerializer, UserSerializer


class ItemSerializer(serializers.ModelSerializer):
    # author = UserdataSerializer(many=False, read_only=True)
    # icon = IconSerializer(many=False, read_only=True)
    # author = serializers.SerializerMethodField()
    # icon = serializers.SerializerMethodField()
    icon = IconSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = models.Item
        fields = ('pk', 'author', 'name', 'icon', 'user_comment', 'position', 'amount', 'unit', 'dday', 'ddate', 'category', 'exist', 'create_type', 'created_at', 'updated_at')

    # def get_author(self, obj):
    #     from common.serializers import UserdataSerializer
    #     return UserdataSerializer(obj.user, many=False, read_only=True).data

    # def get_icon(self, obj):
    #     from common.serializers import IconSerializer
    #     return IconSerializer(obj.icon, many=False, read_only=True).data


class BasicItemSerializer(serializers.ModelSerializer):
    # author = UserdataSerializer(many=False, read_only=True)
    # icon = IconSerializer(many=False, read_only=True)
    # author = serializers.SerializerMethodField()
    icon = IconSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = models.BasicItem
        fields = ('pk', 'author', 'name', 'icon', 'user_comment', 'position', 'exist', 'created_at', 'updated_at')
        # fields = '__all__'

    # def get_author(self, obj):
    #     from common.serializers import UserdataSerializer
    #     return UserdataSerializer(obj, many=False, read_only=True).data

    # def get_icon(self, obj):
    #     from common.serializers import IconSerializer
        # return IconSerializer(obj, many=False, read_only=True).data

class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Memo
        fields = ('pk', 'refrigerator', 'color', 'content', 'created_at', 'updated_at')


class RefrigeratorSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    item_set = ItemSerializer(many=True, read_only=True, required=False)
    basic_item_set = BasicItemSerializer(many=True, read_only=True, required=False)
    memo_set = MemoSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Refrigerator
        fields = ('pk', 'owner', 'item_num', 'item_set', 'basic_item_num', 'basic_item_set', 'memo_num', 'memo_set', 'cool_refrige_item_num', 'freeze_refrige_item_num', 'room_temp_item_num', 'created_at', 'updated_at')

# new_pw = request.data['new_password']
#         new_pw_confirm = request.data['new_password_confirm']
#         if new_pw == new_pw_confirm:
#             user.set_password(new_pw)
#             user.save()
#             auth.login(request, user)
#             Response({
#                 'success': 'true',
#                 'msg': '비밀번호가 변경되었습니다.'
#             }, status=status.HTTP_200_OK)