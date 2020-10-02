from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from rest_framework import status, viewsets, renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models, serializers
from common.models import Icon

# Create your views here.

authentication = TokenAuthentication
if getattr(settings, 'DEBUG', 'False'):
    authentication = BasicAuthentication

class RefrigeratorDetailView(APIView):  # serializer source : owner
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        get #pk refrigerator info
        """
        user = self.request.user
        refri = get_object_or_404(models.Refrigerator, user=user)
        serializer = serializers.RefrigeratorSerializer(refri)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def put(self, request, pk, format=None):
    #     """

    #     """
    #     user = self.request.user
    #     refri = models.Refrigerator.objects.get(pk=pk)
    #     refri.
    #     return

    # def delete(self, request, pk, format=None):
    #     """
    #     """
    #     return

class ItemListView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user
        itemlist = models.Item.objects.filter(author=user).order_by('-updated_at')
        serializer = serializers.ItemSerializer(itemlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        data = {
            name: string,
            user_comment: string,
            icon: number
            position: number // 0: 냉장, 1: 냉동, 2: 실온
            amount: number
            unit: string
            category: number
            dday: number
            ddate: string // ex) 960313
        }
        """
        user = self.request.user
        name = request.data['name']
        user_comment = request.data['user_comment']
        icon = get_object_or_404(Icon, pk=request.data['icon'])
        position = request.data['position']
        amount = request.data['amount']
        unit = request.data['unit']
        category = request.data['category']
        dday = request.data['dday']
        ddate = request.data['ddate']

        item = models.Item.objects.create(
            author=user,
            icon=icon,
            name=name,
            user_comment=user_comment,
            position=position,
            amount=amount,
            unit=unit,
            category=category,
            exist=True,
            ddate=ddate,
            dday=dday,
        )

        refrigerator = get_object_or_404(models.Refrigerator, user=user)
        refrigerator.item_num += 1
        if item.position == 0:
            refrigerator.cool_refrige_item_num += 1
        elif item.position == 1:
            refrigerator.freeze_refrige_item_num += 1
        elif item.position == 2:
            refrigerator.room_temp_item_num += 1
        refrigerator.save()

        serializer = serializers.ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ItemDetailView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        item = get_object_or_404(models.Item, pk=pk)
        serializer = serializers.ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        item = get_object_or_404(models.Item, pk=pk)
        serializer = serializers.ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "msg": "wrong parameters",
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.request.user
        item = get_object_or_404(models.Item, pk=pk)

        refrigerator = get_object_or_404(models.Refrigerator, user=user)
        refrigerator.item_num -= 1
        if item.position == 0:
            refrigerator.cool_refrige_item_num -= 1
        elif item.position == 1:
            refrigerator.freeze_refrige_item_num -= 1
        elif item.position == 2:
            refrigerator.room_temp_item_num -= 1
        refrigerator.save()

        item.delete()
        return Response({
            "success": True,
            "msg": "삭제되었습니다."
        }, status=status.HTTP_200_OK)

class BasicItemListView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user
        basicitemlist = models.BasicItem.objects.filter(author=user).order_by('-updated_at')
        serializer = serializers.BasicItemSerializer(basicitemlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        data = {
            name: string,
            user_comment: string,
            icon: number
            position: number // 0: 냉장, 1: 냉동, 2: 실온
        }
        """
        user = self.request.user
        name = request.data['name']
        user_comment = request.data['user_comment']
        icon = get_object_or_404(Icon, pk=request.data['icon'])
        position = request.data['position']

        basicitem = models.BasicItem.objects.create(
            author=user,
            icon=icon,
            name=name,
            user_comment=user_comment,
            position=position,
            exist=True,
        )

        refrigerator = get_object_or_404(models.Refrigerator, user=user)
        refrigerator.item_num += 1
        if basicitem.position == 0:
            refrigerator.cool_refrige_item_num += 1
        elif basicitem.position == 1:
            refrigerator.freeze_refrige_item_num += 1
        elif basicitem.position == 2:
            refrigerator.room_temp_item_num += 1
        refrigerator.save()

        serializer = serializers.ItemSerializer(basicitem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BasicItemDetailView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        item = get_object_or_404(models.BasicItem, pk=pk)
        serializer = serializers.BasicItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        item = get_object_or_404(models.BasicItem, pk=pk)
        serializer = serializers.BasicItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "msg": "wrong parameters",
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.request.user
        basicitem = get_object_or_404(models.BasicItem, pk=pk)

        refrigerator = get_object_or_404(models.Refrigerator, user=user)
        refrigerator.item_num -= 1
        if basicitem.position == 0:
            refrigerator.cool_refrige_item_num -= 1
        elif basicitem.position == 1:
            refrigerator.freeze_refrige_item_num -= 1
        elif basicitem.position == 2:
            refrigerator.room_temp_item_num -= 1
        refrigerator.save()

        basicitem.delete()
        return Response({
            "success": True,
            "msg": "삭제되었습니다."
        }, status=status.HTTP_200_OK)

class MemoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Memo.objects.order_by('-created_at')
    serializer_class = serializers.MemoSerializer

    def perform_create(self, serializer):
        user = self.request.user
        refrigerator = get_object_or_404(models.Refrigerator, user=user)
        refrigerator.memo_num += 1
        refrigerator.save()
        return super().perform_create(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        refrigerator = get_object_or_404(models.Refrigerator, user=user)
        refrigerator.memo_num -= 1
        refrigerator.save()
        return super().perform_destroy(instance)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication])
def create_refrigerator(request):
    return;
