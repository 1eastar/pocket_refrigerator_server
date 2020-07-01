from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
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
        refri = models.Refrigerator.objects.get(user=user)
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


class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Item.objects.order_by('-created_at')
    serializer_class = serializers.ItemSerializer

    def perform_create(self, serializer):
        user = self.request.user
        item = serializer.save()
        refrigerator = models.Refrigerator.objects.get(user=user)
        refrigerator.item_num += 1
        if item.position == 0:
            refrigerator.cool_refrige_item_num += 1
        elif item.position == 1:
            refrigerator.freeze_refrige_item_num += 1
        elif item.position == 2:
            refrigerator.room_temp_item_num += 1
        refrigerator.save()

    def perform_destroy(self, instance):
        user = self.request.user
        item = self.get_object()
        refrigerator = models.Refrigerator.objects.get(user=user)
        refrigerator.item_num -= 1
        if item.position == 0:
            refrigerator.cool_refrige_item_num -= 1
        elif item.position == 1:
            refrigerator.freeze_refrige_item_num -= 1
        elif item.position == 2:
            refrigerator.room_temp_item_num -= 1
        refrigerator.save()
        return super().perform_destroy(instance)

class BasicItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    queryset = models.BasicItem.objects.order_by('-created_at')
    serializer_class = serializers.BasicItemSerializer

    def perform_create(self, serializer):
        user = self.request.user
        item = serializer.save()
        refrigerator = models.Refrigerator.objects.get(user=user)
        refrigerator.basic_item_num += 1
        if item.position == 0:
            refrigerator.cool_refrige_item_num += 1
        elif item.position == 1:
            refrigerator.freeze_refrige_item_num += 1
        elif item.position == 2:
            refrigerator.room_temp_item_num += 1
        refrigerator.save()

    def perform_destroy(self, instance):
        user = self.request.user
        item = self.get_object()
        refrigerator = models.Refrigerator.objects.get(user=user)
        refrigerator.basic_item_num -= 1
        if item.position == 0:
            refrigerator.cool_refrige_item_num -= 1
        elif item.position == 1:
            refrigerator.freeze_refrige_item_num -= 1
        elif item.position == 2:
            refrigerator.room_temp_item_num -= 1
        refrigerator.save()
        return super().perform_destroy(instance)


class MemoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Memo.objects.order_by('-created_at')
    serializer_class = serializers.MemoSerializer

    def perform_create(self, serializer):
        user = self.request.user
        refrigerator = models.Refrigerator.objects.get(user=user)
        refrigerator.memo_num += 1
        refrigerator.save()
        return super().perform_create(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        refrigerator = models.Refrigerator.objects.get(user=user)
        refrigerator.memo_num -= 1
        refrigerator.save()
        return super().perform_destroy(instance)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication])
def create_refrigerator(request):
    return;
