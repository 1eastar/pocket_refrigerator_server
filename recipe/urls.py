from django.contrib import admin
from django.urls import path, include

from rest_framework  import routers

from . import views

router = routers.DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('comment', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recipestore/<int:pk>/', views.UserRecipeStoreView.as_view()),
    path('recipehistory/<int:pk>/', views.UserRecipeHistoryView.as_view()),
    path('recipeitems/', views.RecipeItemListView.as_view()),
    path('recipeitems/<int:pk>/', views.RecipeItemDetailView.as_view()),
]
