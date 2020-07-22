from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.apps import apps
from django.conf import settings

from rest_framework import status, viewsets, renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models, serializers
from refri.models import BasicItem, Item

# Create your views here.

# authentication = TokenAuthentication
# if getattr(settings, 'DEBUG', 'False'):
#     authentication = BasicAuthentication
authentication = BasicAuthentication

class RecipeViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Recipe.objects.order_by('-updated_at')
    serializer_class = serializers.RecipeSerializer

    def perform_create(self, serializer):
        # serializer.save()
        return super().perform_create(serializer)

    @action(detail=False, methods=['GET'])
    def bestRecipe(self, request):
        recipes = models.Recipe.objects.order_by('like_num')
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def like(self, request, pk):
        user = self.request.user
        like_instance = models.Like.objects.get(author=user)
        if like_instance.exists():
            return Response({
                "success": False,
                "msg": "이미 좋아요를 누르셨습니다."
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        recipe = self.get_object()
        recipe.like_num += 1
        recipe.save()
        newLike = models.Like.objects.create(author=user, recipe=recipe)
        recipe_serializer = serializers.RecipeSerializer(recipe)
        return Response(recipe_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def cancel_like(self, request, pk):
        """
        좋아요 안 눌렀을 때는 좋아요 기능을 함.
        * 없앨까 고민
        """
        user = self.request.user
        like_instance = models.Like.objects.get(author=user)
        if not like_instance.exists():
            recipe = self.get_object()
            recipe.like_num += 1
            recipe.save()
            newLike = models.Like.objects.create(author=user, recipe=recipe)
            recipe_serializer = serializers.RecipeSerializer(recipe)
            return Response(recipe_serializer.data, status=status.HTTP_200_OK)
        recipe = self.get_object()
        if recipe.like_num > 1:
            recipe.like_num -= 1
            recipe.save()
        like = models.Like.objects.get(recipe=recipe, author=user)
        like.delete()

        recipe_serializer = serializers.RecipeSerializer(recipe)
        return Response(recipe_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def report(self, request, pk):
        """
        data = {
            type: number,
            category: number,
            content: string,
            object_id: number,
        }
        """
        recipe = self.get_object()
        recipe.report_num += 1
        recipe.save()
        Report = apps.get_model('common', 'Report')
        newReport = Report.objects.create(report_type=self.request.data['type'], report_category=self.request.data['category'], content=self.request.data['content'], author=self.request.user, report_object_id=self.request.data['object_id'])
        
        report_serializer = serializers.RecipeReportSerializer(newReport)
        return Response(report_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def visit(self, request, pk):
        recipe = self.get_object()
        recipe.visit_num += 1
        recipe.save()
        serializer = serializers.RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RecipeItemListView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        get url parameters = {
            recipe_id: number,
        }
        """
        user = self.request.user
        recipe = models.Recipe.objects.get(pk=self.request.GET.get('recipe_id'))
        recipe_items = models.RecipeItem.objects.filter(recipe=recipe)
        # recipe_items = models.RecipeItem.objects.all()
        serializer = serializers.RecipeItemSerializer(recipe_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        data = {
            amount: number,
            recipe_id: number,
            item_id?: number,
            basic_item_id?: number,
        }
        """
        amount = request.data['amount']
        recipe_id = request.data['recipe_id']
        item_id = request.data['item_id']
        basic_item_id = request.data['basic_item_id']
        if not item_id and not basic_item_id:
            return Response({
                "success": False,
                "msg": "item 또는 basic item들 중 하나를 선택해야합니다."
            })

        recipe = models.Recipe.objects.get(pk=recipe_id)
        if not item_id:
            basic_item = BasicItem.objects.get(pk=basic_item_id)
            recipe_item = models.RecipeItem.objects.create(amount=amount, recipe=recipe, basic_item=basic_item)
        else:
            item = Item.objects.get(pk=item_id)
            recipe_item = models.RecipeItem.objects.create(amount=amount, recipe=recipe, item=item)

        serializer = serializers.RecipeItemSerializer(recipe_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RecipeItemDetailView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.RecipeItem.objects.get(pk=pk)
        except models.RecipeItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        recipe_item = self.get_object(pk)
        serializer = serializers.RecipeItemSerializer(recipe_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        recipe_item = self.get_object(pk)
        serializer = serializers.RecipeItemSerializer(recipe_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errer, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, requsst, pk, format=None):
        recipe_item = self.get_object(pk)
        recipe_item.delete()
        return Response({
            "success": True,
            "msg": "삭제되었습니다."
        }, status=status.HTTP_204_NO_CONTENT)


class UserRecipeStoreView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        user = request.user
        user_recipe_store = models.UserRecipeStore.objects.filter(user=user)
        serializer = serializers.UserRecipeStoreSerializer(user_recipe_store)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'success': 'false',
            'msg': 'serializer is not valid'
        })

    def post(self, request, pk, format=None):
        """
        data = {
            recipe_id: number,
        }
        """
        recipe = models.Recipe.objects.get(id=self.request.data['recipe_id'])
        user = self.request.user
        newURStore = models.UserRecipeStore.objects.create(user=user, recipe=recipe)
        serializer = serializers.UserRecipeStoreSerializer(newURStore)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        """
        ?recipe_id=number : url parameter
        """
        user = request.user
        recipe = models.Recipe.objects.get(id=request.GET.get('recipe_id'))
        URStore = models.UserRecipeStore.objects.get(user=user, recipe=recipe)
        URStore.delete()
        return Response({
            'success': 'true',
            'msg': 'successfully deleted',
        }, status=status.HTTP_204_NO_CONTENT)

class UserRecipeHistoryView(APIView):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        user = request.user
        user_recipe_history = models.UserRecipeHistory.objects.filter(user=user)
        serializer = serializers.UserRecipeHistorySerializer(user_recipe_history)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'success': 'false',
            'msg': 'serializer is not valid'
        })

    def post(self, request, pk, format=None):
        """
        data = {
            recipe_id: number, ?????????????????? post 따로 해야하지 않나?
        }
        """
        recipe = models.Recipe.objects.get(id=self.request.data['recipe_id'])
        user = self.request.user
        newUHStore = models.UserRecipeHistory.objects.create(user=user, recipe=recipe)
        serializer = serializers.UserRecipeHistorySerializer(newUHStore)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        """
        ?recipe_id=number : url parameter
        """
        user = request.user
        recipe = models.Recipe.objects.get(id=request.GET.get('recipe_id'))
        UHStore = models.UserRecipeHistory.objects.get(user=user, recipe=recipe)
        UHStore.delete()
        return Response({
            'success': 'true',
            'msg': 'successfully deleted',
        }, status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Comment.objects.order_by('-created_at')
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save()
        _recipe = comment.recipe
        _recipe.comment_num += 1
        _recipe.save()
        return serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        comment = instance
        _recipe = comment.recipe
        _recipe.comment_num -= 1
        _recipe.save()
        return super().perform_destroy(instance)

    @action(detail=True, methods=['POST'])
    def report(self, request, pk):
        """
        data = {
            type: number,
            category: number,
            content: string,
            object_id: number,
        }
        """
        comment = self.get_object()
        comment.report_num += 1
        comment.save()
        newReport = models.Comment.objects.create(report_type=self.request.data['type'], report_category=self.request.data['category'], content=self.request.data['content'], author=self.request.user, report_object_id=self.request.data['object_id'])
        
        comment_serializer = serializers.CommentSerializer(comment)
        comment_serializer.save(author=self.request.user)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)


